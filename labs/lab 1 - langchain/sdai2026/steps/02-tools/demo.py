"""
STEP 02: An LLM with tools (agentic loop)
=========================================
Building on step 01, we give the LLM TOOLS: Python functions it can decide to call.

`create_agent` builds the classic AGENTIC LOOP for us:

    LLM  --(tool call)-->  tool  --(result)-->  LLM  --(tool call)--> ...  -->  final answer

LangChain calls this object an "agent". In this lab we call it an agentic loop: an LLM that
decides which tools to call. "Agents" in the multi-agent-systems sense (autonomous entities
with beliefs, goals and plans) are something more -- see the last slides.

    uv run steps/02-tools/demo.py
"""

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from lab.config import MODEL, REASONING
from lab.display import banner, print_trace


# 1. Tools: plain functions + @tool.
#    The NAME, the TYPE HINTS and the DOCSTRING are what the model sees!
@tool
def add(x: int, y: int) -> int:
    """Adds 2 numbers and returns the result"""
    return x + y


@tool
def multiply(x: int, y: int) -> int:
    """Multiplies 2 numbers and returns the result"""
    return x * y


tools = [add, multiply]

# 2. The model. temperature=0 makes tool use more reliable
model = ChatOllama(model=MODEL, temperature=0, reasoning=REASONING)

# 3. The agentic loop = model + tools + a loop (LangChain names it an "agent")
assistant = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a careful assistant. Always use the tools to do arithmetic, never compute in your head.",
)

if __name__ == "__main__":
    # What does the model actually see? The JSON schema generated from each tool:
    banner("TOOL SCHEMA SENT TO THE MODEL")
    print(add.name, "-", add.description, "-", add.args)

    question = "What is 5 + 3, and then multiply the result by 2?"
    answer = assistant.invoke({"messages": [{"role": "user", "content": question}]})

    # The result contains ALL the messages of the loop, not only the final answer
    banner("TRACE OF THE AGENTIC LOOP")
    print_trace(answer["messages"])

    banner("FINAL ANSWER")
    print(answer["messages"][-1].content)
