"""
Shared configuration for every step of the lab  (import it with: from lab.config import MODEL).

Change the model in ONE place (or with an environment variable):

    LAB_MODEL=llama3.2 uv run steps/01-chain/demo.py

The model must support *tool calling* for steps 02 and 04.
Good small choices: qwen3:4b-instruct (default), llama3.2:3b, qwen2.5:7b.
Avoid "thinking-only" models (e.g. plain qwen3:4b) for agentic loops: they reason for minutes at every step.
"""

import os

# Ollama model used by all the scripts
MODEL = os.getenv("LAB_MODEL", "qwen3:4b-instruct")

# Where the Ollama server is listening (default local install)
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Where the mock REST API of the lab is listening (services/mock_api.py)
MOCK_API_URL = os.getenv("MOCK_API_URL", "http://localhost:8765")

# "Thinking" models (qwen3, deepseek-r1, gpt-oss...) reason before answering.
#   unset            -> model default; Ollama keeps the reasoning OUT of the answer   (recommended)
#   LAB_REASONING=1  -> reasoning on, available in message.additional_kwargs["reasoning_content"]
#   LAB_REASONING=0  -> ask the model not to think (faster, only for models that support it)
_reasoning = os.getenv("LAB_REASONING")
REASONING = None if _reasoning is None else _reasoning == "1"
