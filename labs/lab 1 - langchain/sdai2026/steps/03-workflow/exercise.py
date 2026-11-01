"""
STEP 03 — EXERCISE
==================
Start from the workflow of demo.py and add a FEEDBACK LOOP.

Exercise 3.1 — A critic with a conditional edge
    Add a `critic` node after the writer. The critic reads the article and replies
    with "APPROVED" or with "REVISE: <what to improve>".
      - if APPROVED                      -> END
      - if REVISE and revisions < 2      -> back to the writer, which must use the feedback
      - otherwise                        -> END  (always put a limit on loops!)
    You need: new state keys (`feedback`, `revisions`), a routing function and
    `workflow.add_conditional_edges("critic", route, {...})`.

Exercise 3.2 — Visualise the graph
    Print `app.get_graph().draw_mermaid()` and paste the output into https://mermaid.live
    Do you see the loop?

    uv run steps/03-workflow/exercise.py
"""

from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

from lab.config import MODEL, REASONING
from lab.display import banner


class State(TypedDict):
    topic: str
    research: str
    analysis: str
    final_output: str
    # TODO (3.1): add `feedback: str` and `revisions: int`
    feedback: str
    revisions: int


model = ChatOllama(model=MODEL, temperature=0.3, reasoning=REASONING)


def ask_llm(role: str, task: str) -> str:
    response = model.invoke([SystemMessage(content=role), HumanMessage(content=task)])
    return response.content


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
    task = (
        f"Based on this analysis, write a clear and engaging article of about 150 words "
        f"about '{state['topic']}'.\n\n{state['analysis']}"
    )
    # TODO (3.1): if there is feedback from the critic, add the previous article and the
    #             feedback to the task, and increment `revisions` in the returned dict
    revisions = state.get("revisions", 0)
    must_revise = (
        state.get("feedback") and state.get("feedback") != "APPROVED" and revisions < 2
    )

    if must_revise:
        print("📝 writer is revising the article based on feedback...")
        task += f"\n\nThe previous article was:\n{state.get('final_output')}\n\nThe feedback from the critic was:\n{state.get('feedback')}"
        revisions += 1

    text = ask_llm("You are a professional science writer.", task)
    return {"final_output": text, "revisions": revisions}


# TODO (3.1): the critic node — returns {"feedback": "APPROVED" | "REVISE: ..."}
def critic(state: State) -> dict:
    print("🧐 critic is reviewing the article...")
    system_prompt = (
        "You are a critical reviewer of scientific articles. "
        "You will read the article and provide feedback. "
        "Be really really critical and specific, you must not accept vague or imperfect articles. "
        "If the article is good, reply with 'APPROVED'. "
        "If it needs improvement, reply with 'REVISE: <what to improve>'."
    )
    user_prompt = f"Please review the following article and provide feedback:\n\n{state['final_output']}"

    feedback = ask_llm(system_prompt, user_prompt)
    return {"feedback": feedback}


# TODO (3.1): the routing function — returns the NAME of the next node (or END)
def route_after_critic(state: State) -> str:
    feedback = state.get("feedback", "")
    revisions = state.get("revisions", 0)

    if feedback == "APPROVED":
        return END
    if feedback.startswith("REVISE") and revisions < 2:
        return "writer"

    return END


workflow = StateGraph(State)
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("writer", writer)
# TODO (3.1): add the critic node
workflow.add_node("critic", critic)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
# workflow.add_edge(
#     "writer", END
# )
# TODO (3.1): writer -> critic, then a conditional edge from the critic
workflow.add_edge("writer", "critic")
workflow.add_conditional_edges(
    "critic", route_after_critic, {END: END, "writer": "writer"}
)

app = workflow.compile()

if __name__ == "__main__":
    # TODO (3.2): print the mermaid diagram of the graph
    print(app.get_graph().draw_mermaid())

    # TODO (3.1): initialise revisions=0 in the input
    result = app.invoke(
        {"topic": "The benefits of artificial intelligence in medicine", "revisions": 0}
    )

    banner("FINAL OUTPUT")
    print(result["final_output"])
