"""
STEP 01 — EXERCISE
==================
Start from the chain of demo.py and extend it.

Exercise 1.1 — More template variables
    Add a {audience} variable to the prompt so that the same question can be explained
    "to a 10-year-old" or "to a physics PhD student". Invoke the chain twice and compare.

Exercise 1.2 — Structured output
    Free text is hard to use in a program. Make the model return a Python object instead:
    complete the `Explanation` Pydantic model and build `structured_chain` with
    `llm.with_structured_output(Explanation)`. Print the fields separately.

    uv run steps/01-chain/exercise.py
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from lab.config import MODEL, REASONING

llm = ChatOllama(model=MODEL, temperature=0.0, reasoning=REASONING)


# ---------------------------------------------------------------------------
# Exercise 1.1
# ---------------------------------------------------------------------------
# TODO (1.1): add an {audience} placeholder to the system message
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant who answers clearly and concisely."),
        ("user", "{input}"),
        ("user", "Explain it to a {audience}."),
    ]
)

chain = prompt | llm | StrOutputParser()


# ---------------------------------------------------------------------------
# Exercise 1.2
# ---------------------------------------------------------------------------
class Explanation(BaseModel):
    """A short explanation of a topic."""

    title: str = Field(description="A catchy title for the explanation")
    # TODO (1.2): add a `summary` (str) and a `keywords` (list[str]) field,
    #             each one with a Field(description=...) — the description is sent to the model!
    summary: str = Field(description="A concise summary of the topic max 2 sentences")
    keywords: list[str] = Field(description="A list of relevant keywords for the topic")


# TODO (1.2): build the structured chain:  prompt | llm.with_structured_output(Explanation)
structured_chain = prompt | llm.with_structured_output(Explanation)


if __name__ == "__main__":
    question = "Explain the theory of relativity."
    audiences = ["10-year-old", "physics PhD student"]

    def explain_to_audience(audience: str):
        # TODO (1.1): invoke `chain` for two different audiences and print the answers
        print(f"\n--- Explaining to {audience} ---")
        inv_params = {"input": question, "audience": audience}
        print(chain.invoke(inv_params))

        print(f"\n--- Structured explanation to {audience} ---")
        # TODO (1.2): invoke `structured_chain`, then print result.title, result.summary, result.keywords
        result = structured_chain.invoke(inv_params)
        for field in result.model_fields:  # pyright: ignore[reportAttributeAccessIssue]
            print(f" - {field}: {getattr(result, field)}\n")
        print("\n\n")

    for audience in audiences:
        explain_to_audience(audience)
