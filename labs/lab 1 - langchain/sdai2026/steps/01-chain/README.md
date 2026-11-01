# Step 01 · Chain  (20')

**Goal:** talk to a local LLM from Python and compose the basic building blocks of LangChain.

```
{"input": "..."}  →  ChatPromptTemplate  →  ChatOllama  →  StrOutputParser  →  "text"
```

## Concepts
- **ChatOllama** — a chat model served by the local Ollama server (`lab/config.py` chooses which one).
- **Prompt template** — messages with `{placeholders}` filled in at `invoke` time.
- **LCEL pipe `|`** — every block is a *Runnable*; `a | b` feeds the output of `a` into `b`.
  Every chain has `.invoke()`, `.stream()` and `.batch()`.
- **Structured output** — `llm.with_structured_output(PydanticModel)` makes the model fill a schema:
  you get a Python object, not a string. (Under the hood: JSON schema + constrained decoding.)

## Run
```bash
uv run steps/01-chain/demo.py
```

## Exercise — `exercise.py`
1. **1.1 · More template variables.** Add an `{audience}` variable to the prompt so the same question can be
   explained *"to a 10-year-old"* or *"to a physics PhD student"*. Invoke the chain twice and compare.
2. **1.2 · Structured output.** Complete the `Explanation` Pydantic model (`title`, `summary`, `keywords: list[str]`)
   and build `structured_chain = prompt | llm.with_structured_output(Explanation)`. Print each field separately.

*Questions to think about:* what happens to the answers if you set `temperature=0`? What if you remove the
`Field(description=...)`?
