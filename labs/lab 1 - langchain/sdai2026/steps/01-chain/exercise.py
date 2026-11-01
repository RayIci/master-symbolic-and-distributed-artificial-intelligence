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

llm = ChatOllama(model=MODEL, temperature=0.7, reasoning=REASONING)


# ---------------------------------------------------------------------------
# Exercise 1.1
# ---------------------------------------------------------------------------
# TODO (1.1): add an {audience} placeholder to the system message
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who answers clearly and concisely."),
    ("user", "{input}"),
])

chain = prompt | llm | StrOutputParser()


# ---------------------------------------------------------------------------
# Exercise 1.2
# ---------------------------------------------------------------------------
class Explanation(BaseModel):
    """A short explanation of a topic."""

    title: str = Field(description="A catchy title for the explanation")
    # TODO (1.2): add a `summary` (str) and a `keywords` (list[str]) field,
    #             each one with a Field(description=...) — the description is sent to the model!


# TODO (1.2): build the structured chain:  prompt | llm.with_structured_output(Explanation)
structured_chain = None


if __name__ == "__main__":
    question = "Explain the theory of relativity."

    # TODO (1.1): invoke `chain` for two different audiences and print the answers
    print(chain.invoke({"input": question}))

    # TODO (1.2): invoke `structured_chain`, then print result.title, result.summary, result.keywords
    if structured_chain is not None:
        result = structured_chain.invoke({"input": question})
        print(type(result), result)
