"""
STEP 01: Basic LLM Chain
========================
The simplest way of using a local model with LangChain.
We build a *chain*:   Prompt  ->  LLM  ->  Output Parser

    uv run steps/01-chain/demo.py
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from lab.config import MODEL, REASONING

# 1. The local LLM served by Ollama
llm = ChatOllama(model=MODEL, temperature=0.7, reasoning=REASONING)

# 2. A prompt TEMPLATE: {input} is filled in at invocation time
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who answers clearly and concisely."),
    ("user", "{input}"),
])

# 3. The chain: the output of each block is the input of the next one (LCEL "pipe" syntax)
chain = prompt | llm | StrOutputParser()

if __name__ == "__main__":
    # 4. Run it
    result = chain.invoke({"input": "Explain the theory of relativity in an easy way, in 5 sentences."})
    print(result)

    # Bonus: the same chain can stream tokens as they are generated
    print("\n--- streaming ---")
    for token in chain.stream({"input": "Give me 3 fun facts about llamas."}):
        print(token, end="", flush=True)
    print()
