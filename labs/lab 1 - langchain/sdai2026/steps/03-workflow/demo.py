"""
STEP 03: A workflow of LLM roles
================================
Building on step 01/02, we now create a WORKFLOW where several LLM calls with different ROLES collaborate.
Each one has a specific role:   Researcher  ->  Analyst  ->  Writer

The roles communicate through a shared STATE, and LangGraph runs the graph for us.

    uv run steps/03-workflow/demo.py
"""

from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

from lab.config import MODEL, REASONING
from lab.display import banner


# 1. Shared state: every node READS from it and RETURNS the keys it wants to UPDATE
class State(TypedDict):
    topic: str
    research: str
    analysis: str
    final_output: str


# The model is shared by all the roles: what changes is the system prompt
model = ChatOllama(model=MODEL, temperature=0.3, reasoning=REASONING)


def ask_llm(role: str, task: str) -> str:
    response = model.invoke([SystemMessage(content=role), HumanMessage(content=task)])
    return response.content


# 2. Nodes: plain functions  State -> partial State
def researcher(state: State) -> dict:
    print("🔎 researcher is working...")
    text = ask_llm(
        "You are an experienced researcher. Be factual and concise.",
        f"Collect the most important facts (max 8 bullet points) about: {state['topic']}",
    )
    return {"research": text}


def analyst(state: State) -> dict:
    print("📊 analyst is working...")
    text = ask_llm(
        "You are a skilled analyst.",
        f"Analyze the following research. Identify the 3 key insights and one open problem.\n\n{state['research']}",
    )
    return {"analysis": text}


def writer(state: State) -> dict:
    print("📝 writer is working...")
    text = ask_llm(
        "You are a professional science writer.",
        f"Based on this analysis, write a clear and engaging article of about 150 words "
        f"about '{state['topic']}'.\n\n{state['analysis']}",
    )
    return {"final_output": text}


# 3. The graph: nodes + edges
workflow = StateGraph(State)
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("writer", writer)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

# 4. Compile it into a Runnable (same .invoke / .stream interface as a chain!)
app = workflow.compile()

if __name__ == "__main__":
    result = app.invoke(
        {"topic": "The benefits of artificial intelligence in medicine"}
    )

    banner("RESEARCHER")
    print(result["research"])
    banner("ANALYST")
    print(result["analysis"])
    banner("WRITER (final output)")
    print(result["final_output"])
