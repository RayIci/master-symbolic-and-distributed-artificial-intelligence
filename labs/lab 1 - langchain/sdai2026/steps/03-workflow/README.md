# Step 03 · Workflow  (30')

**Goal:** make several LLM calls with different **roles** collaborate in a **graph** built with LangGraph.

```
START ─▶ researcher ─▶ analyst ─▶ writer ─▶ END
```

## Concepts
- **State** — a `TypedDict` shared by all the nodes. Each node reads it and returns **only the keys it updates**.
- **Node** — a plain Python function `State -> dict`. Here every node is an LLM call with a different
  *role* (system prompt), but a node can be anything (a tool, a whole agentic loop, a human…).
- **Edges** — `add_edge(a, b)` fixed transitions; `add_conditional_edges(a, router, mapping)` lets a
  function decide the next node at runtime → **branches and loops**.
- **Compile** — `workflow.compile()` returns a Runnable: `.invoke()`, `.stream()`, `.get_graph()`.
- **Workflow vs agentic loop** — here *we* decide the control flow (predictable). In step 02 the *LLM* decided it.

## Run
```bash
uv run steps/03-workflow/demo.py
```

## Exercise — `exercise.py`
1. **3.1 · A critic with a conditional edge.** Add a `critic` node after the writer that answers `APPROVED` or
   `REVISE: <what to improve>`. Route back to the writer (which must use the feedback) if a revision is needed,
   **at most 2 times**, otherwise go to `END`. You need new state keys (`feedback`, `revisions`), a routing
   function and `add_conditional_edges`.
2. **3.2 · Visualise the graph.** Print `app.get_graph().draw_mermaid()` and paste it into
   <https://mermaid.live>. Do you see the loop?

*Think about:* why is the `revisions` limit essential? What happens with a small model if you remove it?
