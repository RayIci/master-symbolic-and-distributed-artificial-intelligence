"""
STEP 04: Agentic workflow
=========================
Step 02 (LLMs that use tools)  +  Step 03 (a graph of collaborating LLM roles).

Every node of the graph now runs its own AGENTIC LOOP with specialised tools:

    START -> 🔎 researcher [web_search, get_statistics]
          -> 📊 analyst    [calculate_percentage, calculate_growth, get_statistics]
          -> 📝 writer     (no tools: not every node needs an agentic loop!)
          -> END

Start the mock API first (second terminal):   uv run services/mock_api.py

    uv run steps/04-agentic-workflow/demo.py
"""

from typing import TypedDict

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

from lab.config import MODEL, REASONING
from lab.display import banner, print_trace
from tools import calculate_growth, calculate_percentage, get_statistics, web_search


class State(TypedDict):
    topic: str
    research: str
    analysis: str
    report: str


model = ChatOllama(model=MODEL, temperature=0, reasoning=REASONING)

# Specialised agentic loops: same model, different tools and instructions
researcher_llm = create_agent(
    model=model,
    tools=[web_search, get_statistics],
    system_prompt=(
        "You are a research specialist. Use web_search (one or two short queries) and get_statistics "
        "to gather facts and numbers. Then summarise your findings as bullet points with the sources' numbers. "
        "Only report information returned by the tools."
    ),
)

analyst_llm = create_agent(
    model=model,
    tools=[calculate_percentage, calculate_growth, get_statistics],
    system_prompt=(
        "You are a data analyst. Use the calculation tools to compute growth rates and percentages "
        "from the numbers in the research. Never do arithmetic in your head. Report the computed metrics "
        "and what they imply."
    ),
)


def run_with_tools(llm, name: str, task: str) -> str:
    """Runs an agentic loop, shows which tools it used, returns its final answer."""
    print(f"\n{name} is working...")
    result = llm.invoke({"messages": [{"role": "user", "content": task}]})
    print_trace(result["messages"], tools_only=True)
    return result["messages"][-1].content


def researcher(state: State) -> dict:
    return {"research": run_with_tools(researcher_llm, "🔎 researcher", f"Research this topic: {state['topic']}")}


def analyst(state: State) -> dict:
    task = f"Analyse the data in this research about '{state['topic']}':\n\n{state['research']}"
    return {"analysis": run_with_tools(analyst_llm, "📊 analyst", task)}


def writer(state: State) -> dict:
    print("\n📝 writer is working...")
    response = model.invoke(
        "You are a professional technical writer. Write a short executive summary (max 200 words) with: "
        "1) key findings, 2) important statistics, 3) a recommendation.\n\n"
        f"TOPIC: {state['topic']}\n\nRESEARCH:\n{state['research']}\n\nANALYSIS:\n{state['analysis']}"
    )
    return {"report": response.content}


workflow = StateGraph(State)
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("writer", writer)
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)
app = workflow.compile()

if __name__ == "__main__":
    result = app.invoke({"topic": "The impact of artificial intelligence in modern healthcare"})

    banner("🔎 RESEARCH")
    print(result["research"])
    banner("📊 ANALYSIS")
    print(result["analysis"])
    banner("📝 FINAL REPORT")
    print(result["report"])
