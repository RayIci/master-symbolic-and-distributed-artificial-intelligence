"""
STEP 00: Setup check
====================
Run this BEFORE the lab starts:

    uv run scripts/check_setup.py

It verifies, in order:
  1. the Python packages are installed
  2. the Ollama server is running
  3. the lab model has been pulled
  4. the model answers a prompt
  5. the model is able to call a tool (needed from step 02 on)
"""

import sys
import time

import requests

from lab.config import MODEL, OLLAMA_URL, REASONING
from lab.display import BOLD, GREEN, RESET, YELLOW

RED = "\033[31m"


def ok(msg: str) -> None:
    print(f"{GREEN}  [OK]{RESET} {msg}")


def fail(msg: str, hint: str) -> None:
    print(f"{RED}  [FAIL]{RESET} {msg}\n{YELLOW}         -> {hint}{RESET}")
    sys.exit(1)


def main() -> None:
    print(f"{BOLD}Checking lab setup (model: {MODEL}, server: {OLLAMA_URL}){RESET}")

    # 1. Python packages
    try:
        import langchain  # noqa: F401
        import langchain_ollama  # noqa: F401
        import langgraph  # noqa: F401
    except ImportError as e:
        fail(f"Missing package: {e.name}", "run `uv sync` (or `pip install -e .`) from the repo root")
    ok(f"Python {sys.version.split()[0]} and packages langchain / langchain-ollama / langgraph")

    # 2. Ollama server
    try:
        tags = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3).json()
    except requests.RequestException:
        fail(f"Ollama is not reachable at {OLLAMA_URL}", "start the Ollama app, or run `ollama serve` in another terminal")
    ok("Ollama server is running")

    # 3. Model pulled
    names = {m["name"] for m in tags.get("models", [])}
    if MODEL not in names and f"{MODEL}:latest" not in names:
        fail(f"Model '{MODEL}' not found locally", f"run `ollama pull {MODEL}`")
    ok(f"Model '{MODEL}' is available")

    # 4. Simple prompt
    from langchain_ollama import ChatOllama

    model = ChatOllama(model=MODEL, temperature=0, reasoning=REASONING)
    start = time.time()
    answer = model.invoke("Reply with exactly one word: ready")
    ok(f"Model answered '{answer.content.strip()}' in {time.time() - start:.1f}s")

    # 5. Tool calling
    from langchain_core.tools import tool

    @tool
    def add(x: int, y: int) -> int:
        """Adds 2 numbers and returns the result"""
        return x + y

    reply = model.bind_tools([add]).invoke("What is 21 + 21? Use the tool.")
    if not reply.tool_calls:
        fail(f"'{MODEL}' did not call the tool", "choose a model with tool support, e.g. LAB_MODEL=qwen3:4b-instruct or llama3.2")
    ok(f"Tool calling works: {reply.tool_calls[0]['name']}({reply.tool_calls[0]['args']})")

    print(f"\n{GREEN}{BOLD}All good, you are ready for the lab!{RESET}")


if __name__ == "__main__":
    main()
