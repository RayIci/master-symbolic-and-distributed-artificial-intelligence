"""
Pretty-printing helpers, so that the scripts can focus on the agentic logic.

    from lab.display import banner, print_trace
"""

import json

# ANSI colors (work in every modern terminal, including the VS Code / PyCharm ones)
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"


def banner(title: str, width: int = 60) -> None:
    """Prints a section header."""
    print(f"\n{BOLD}{'=' * width}\n{title}\n{'=' * width}{RESET}")


def print_trace(messages, tools_only: bool = False) -> None:
    """
    Prints every message produced during an agentic run, so we can SEE the loop:

        user  ->  AI (asks for a tool)  ->  tool result  ->  AI (asks for a tool)  ->  ...  ->  AI (final answer)

    With tools_only=True only the tool calls and their results are printed.
    """
    for i, msg in enumerate(messages):
        kind = msg.type  # "human" | "ai" | "tool" | "system"
        if tools_only and kind != "tool" and not getattr(msg, "tool_calls", None):
            continue
        if kind == "human":
            print(f"{BLUE}{BOLD}[{i}] USER{RESET}  {msg.content}")
        elif kind == "system":
            print(f"{DIM}[{i}] SYSTEM  {msg.content}{RESET}")
        elif kind == "ai":
            for call in getattr(msg, "tool_calls", None) or []:
                args = json.dumps(call["args"])
                print(f"{YELLOW}{BOLD}[{i}] AI -> TOOL CALL{RESET}  {call['name']}({args})")
            if msg.content and not tools_only:
                print(f"{GREEN}{BOLD}[{i}] AI{RESET}  {msg.content}")
        elif kind == "tool":
            content = msg.content if len(msg.content) < 300 or not tools_only else msg.content[:300] + " ..."
            print(f"{MAGENTA}{BOLD}[{i}] TOOL RESULT{RESET} ({msg.name})  {content}")
        else:
            print(f"[{i}] {kind}: {msg.content}")
