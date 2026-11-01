# Step 04 · Agentic workflow  (25')

**Goal:** combine step 02 and step 03 — every node of the graph now runs its own **agentic loop with its own tools**.

```
START ─▶ 🔎 researcher [web_search, get_statistics]
      ─▶ 📊 analyst    [calculate_percentage, calculate_growth, get_statistics]
      ─▶ 📝 writer     (plain LLM call)
      ─▶ END
```

> Start the mock API first, in a second terminal: `uv run services/mock_api.py`

## Concepts
- **Specialisation** — few tools per agentic loop and a focused system prompt: small models choose tools much
  better among 2–3 options than among 15.
- **Tools live in [`tools.py`](tools.py)** — they call the mock API (`/api/search`, `/api/stats`, `/api/weather`).
  A tool should **never raise**: it returns an error message so the LLM can react.
- **Grounding** — the researcher is told to *only report what the tools returned*: this reduces hallucinations
  (check whether it actually works with a 4B model!).
- **Not every node needs an agentic loop** — the writer has no tools: a plain LLM call is cheaper and more predictable.
- **Routing** — a node can decide *which* part of the graph to run, e.g. using structured output.

## Run
```bash
uv run services/mock_api.py          # terminal 1
uv run steps/04-agentic-workflow/demo.py # terminal 2
```

## Exercise — `exercise.py`
1. **4.1 · A router in front of the workflow.** Add a `router` node at `START` that classifies the request with
   **structured output** (step 01) into `"weather"` or `"report"`, and a **conditional edge** (step 03) that sends
   it either to a new `weather` agentic loop (tool `get_weather`) or to the researcher → analyst → writer pipeline.
2. **4.2 · A new tool for the analyst.** Write `cagr(start_value, end_value, years)` — Compound Annual Growth Rate,
   `(end/start)^(1/years) − 1` — and give it to the analyst. Check in the trace that it is actually used; if not,
   improve its docstring and/or the system prompt.
