"""
STEP 02 — EXERCISE
==================
Start from the agentic loop of demo.py and extend it.

Exercise 2.1 — More tools
    Add `subtract`, `divide` and `power` tools, then ask a question that needs at least
    3 tool calls, e.g. "What is (12 - 4) to the power of 2, divided by 4?".
    Look at the trace: does the model call the tools in the right order?

Exercise 2.2 — A tool that calls a REST API
    Start the mock API in another terminal:   uv run services/mock_api.py
    Implement `get_weather(city)` calling  GET {MOCK_API_URL}/api/weather?city=<city>
    with `requests`, and ask: "Should I bring an umbrella in Bologna or in Rome today?"

Exercise 2.3 — Docstrings matter (discussion)
    Change the docstring of `multiply` to something misleading (e.g. "Adds two numbers")
    or remove the type hints. What happens to the tool calls?

    uv run steps/02-tools/exercise.py
"""

import requests
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from lab.config import MOCK_API_URL, MODEL, REASONING
from lab.display import banner, print_trace


@tool
def add(x: int, y: int) -> int:
    """Adds 2 numbers and returns the result"""
    return x + y


@tool
def multiply(x: int, y: int) -> int:
    """Multiplies 2 numbers and returns the result"""
    return x * y


# TODO (2.1): add the `subtract`, `divide` and `power` tools
#             Hint: what should `divide` return when dividing by zero? (a tool can return an error message!)
@tool
def subtract(x: int, y: int) -> int:
    """Subtracts 2 numbers and returns the result"""
    return x - y


@tool
def divide(x: int, y: int) -> str:
    """Divides 2 numbers and returns the result, or an error message if dividing by zero"""
    if y == 0:
        return "Error: Cannot divide by zero"
    return str(x / y)


# TODO (2.2): implement the weather tool
@tool
def get_weather(city: str) -> str:
    """TODO: write a docstring that tells the model WHEN to use this tool"""
    # Hint: requests.get(f"{MOCK_API_URL}/api/weather", params={"city": city}, timeout=5).json()
    return requests.get(
        f"{MOCK_API_URL}/api/weather", params={"city": city}, timeout=5
    ).json()


# TODO (2.1, 2.2): register all the tools
tools = [add, multiply, subtract, divide, get_weather]

model = ChatOllama(model=MODEL, temperature=0, reasoning=REASONING)

assistant = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a careful assistant. Always use the tools to do arithmetic, never compute in your head.",
)


def ask(question: str) -> None:
    banner(question)
    answer = assistant.invoke({"messages": [{"role": "user", "content": question}]})
    print_trace(answer["messages"])


if __name__ == "__main__":
    ask("What is (12 - 4) to the power of 2, divided by 4?")  # 2.1
    # ask("Should I bring an umbrella in Bologna or in Rome today?")  # TODO (2.2): uncomment
    ask("Should I bring an umbrella in Bologna or in Rome today?")  # sanity check
