# Step 02 · Tools  (30')

**Goal:** put the LLM in an **agentic loop**: it decides *which* function to call, with *which* arguments,
observes the result and keeps going until it can answer.

```
user ─▶ LLM ──tool call──▶ tool ──result──▶ LLM ──tool call──▶ … ──▶ final answer
```

## Concepts
- **`@tool`** — turns a Python function into a tool. The model only sees its **name**, **docstring** and
  **argument schema** (from the type hints): that is the whole "API documentation" for the LLM.
- **Tool calling** — the model does not run code: it outputs a structured *request* (`AIMessage.tool_calls`);
  our program executes it and sends back a `ToolMessage` with the result.
- **`create_agent(model, tools, system_prompt=...)`** — LangChain calls the result an "agent"; we call it an
  **agentic loop** (agents in the multi-agent-systems sense are more than this, see the last slides). It builds the loop *LLM → tools → LLM* and stops
  when the model answers without requesting tools. The result contains **all** the messages of the loop.
- **Tools with side effects** — a tool can do anything Python can: call an API, query a DB, write a file…

## Run
```bash
uv run steps/02-tools/demo.py
# for exercise 2.2, in a second terminal:
uv run services/mock_api.py
```

## Exercise — `exercise.py`
1. **2.1 · More tools.** Add `subtract`, `divide` and `power`, then ask a question that needs at least 3 tool
   calls, e.g. *"What is (12 − 4) to the power of 2, divided by 4?"*. Does the model call them in the right order?
2. **2.2 · A tool that calls a REST API.** Implement `get_weather(city)` calling
   `GET http://localhost:8765/api/weather?city=<city>` with `requests`, then ask
   *"Should I bring an umbrella in Bologna or in Rome today?"*. (Notice: one question, **two** tool calls.)
3. **2.3 · Docstrings matter.** Give `multiply` a misleading docstring (*"Adds two numbers"*) or remove its type
   hints. What happens?
