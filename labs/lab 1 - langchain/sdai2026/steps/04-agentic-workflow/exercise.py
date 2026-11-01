"""
STEP 04 — EXERCISE
==================
Start from the agentic workflow of demo.py and make it smarter.
Mock API needed (second terminal):   uv run services/mock_api.py

Exercise 4.1 — A router in front of the workflow
    The system should handle different kinds of requests:
      - "What's the weather like in Rome?"                        -> a weather assistant  (tool: get_weather)
      - "Write a report on AI adoption in hospitals"              -> researcher -> analyst -> writer
    Add a `router` node at START that classifies the request using STRUCTURED OUTPUT (step 01!)
    into "weather" or "report", and a conditional edge (step 03!) to the right branch.

Exercise 4.2 — A new tool for the analyst
    Write a `cagr(start_value, end_value, years)` tool (Compound Annual Growth Rate:
    (end/start)^(1/years) - 1) and give it to the analyst. Check in the trace that it is used.
    Tip: if the model ignores it, improve the docstring and/or the system prompt.

    uv run steps/04-agentic-workflow/exercise.py
"""

from typing import Literal, TypedDict

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from lab.config import MODEL, REASONING
from lab.display import banner, print_trace
from tools import calculate_growth, calculate_percentage, get_statistics, get_weather, web_search


class State(TypedDict):
    topic: str  # the user request
    research: str
    analysis: str
    report: str
    # TODO (4.1): add a `route` key


model = ChatOllama(model=MODEL, temperature=0, reasoning=REASONING)


# ---------------------------------------------------------------------------
# Exercise 4.2: the CAGR tool
# ---------------------------------------------------------------------------
# TODO (4.2): define the `cagr` tool here (with a good docstring!) and add it to the analyst's tools


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

# TODO (4.1): create a `weather_llm` agentic loop with the get_weather tool
weather_llm = None


def run_with_tools(llm, name: str, task: str) -> str:
    print(f"\n{name} is working...")
    result = llm.invoke({"messages": [{"role": "user", "content": task}]})
    print_trace(result["messages"], tools_only=True)
    return result["messages"][-1].content


# ---------------------------------------------------------------------------
# Exercise 4.1: the router
# ---------------------------------------------------------------------------
# TODO (4.1): explain the two options to the model (it will be the system message of the router)
ROUTER_PROMPT = """You route user requests to the right team. ..."""


class Route(BaseModel):
    """Which team handles the user request."""

    # TODO (4.1): a field `team: Literal["weather", "report"]` with a Field(description=...)
    pass


def router(state: State) -> dict:
    # TODO (4.1): use model.with_structured_output(Route) to classify state["topic"]
    #             (messages: [("system", ROUTER_PROMPT), ("user", state["topic"])])
    #             and return {"route": ...}
    raise NotImplementedError


def weather(state: State) -> dict:
    # TODO (4.1): run weather_llm; put its answer in "report"
    raise NotImplementedError


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
# TODO (4.1): add the "router" and "weather" nodes

workflow.add_edge(START, "researcher")  # TODO (4.1): START -> router -> (conditional) weather | researcher
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)
# TODO (4.1): weather -> END
app = workflow.compile()

if __name__ == "__main__":
    for request in [
        "Write a report on the adoption of AI in hospitals",
        "What's the weather like in Rome? Do I need a jacket?",
    ]:
        banner(f"REQUEST: {request}")
        result = app.invoke({"topic": request})
        banner("ANSWER")
        print(result["report"])
