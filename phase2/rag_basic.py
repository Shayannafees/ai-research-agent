import os
import numpy as np
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── 1. OUR DOCUMENT (split into chunks) ──────────────────────────
chunks = [
    "RAG stands for Retrieval-Augmented Generation. It combines search with LLMs to answer questions grounded in real documents.",
    "Vector databases store embeddings which are numerical representations of text meaning. Similar texts have similar embeddings.",
    "Embeddings are arrays of floating point numbers. A sentence becomes a vector like [0.2, 0.8, 0.1, ...].",
    "LangChain is a framework that simplifies building LLM applications with tools for agents, memory, and retrieval.",
    "FastAPI is a modern Python web framework for building APIs. It is async-friendly and auto-generates documentation.",
]

# ── 2. SIMULATE EMBEDDINGS USING THE LLM ─────────────────────────
# We ask Claude to rate how related each chunk is to a query
# This teaches the concept without needing a separate embeddings API
def find_relevant_chunks(query, chunks, top_k=2):
    chunks_text = "\n".join([f"{i}: {chunk}" for i, chunk in enumerate(chunks)])
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        system="""You are a relevance scoring system. Given a query and numbered chunks,
return only a JSON array of the top chunk indices most relevant to the query.
Example output: [2, 0]
Return only the JSON array, nothing else.""",
        messages=[{
            "role": "user",
            "content": f"Query: {query}\n\nChunks:\n{chunks_text}\n\nReturn the {top_k} most relevant chunk indices as a JSON array."
        }]
    )
    
    raw = response.content[0].text.strip()
    indices = eval(raw)  # safe here since we control the output format
    return [chunks[i] for i in indices]

# ── 3. RAG PIPELINE ──────────────────────────────────────────────
def ask(question):
    print(f"Question: {question}")
    print("Searching for relevant chunks...")
    
    # Step 1: retrieve relevant chunks
    relevant = find_relevant_chunks(question, chunks)
    
    print(f"Found {len(relevant)} relevant chunks:")
    for chunk in relevant:
        print(f"  → {chunk[:60]}...")
    
    # Step 2: build prompt with retrieved context
    context = "\n".join(relevant)
    
    # Step 3: ask the LLM with context injected
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        system="""You are a research assistant. Answer questions using ONLY 
the provided context. If the answer isn't in the context, say so.""",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )
    
    print(f"\nAnswer: {response.content[0].text}\n")
    print("-" * 50 + "\n")

# ── 4. TEST IT ────────────────────────────────────────────────────
ask("What is RAG and how does it work?")
ask("What is FastAPI used for?")
ask("What is the capital of France?")  # not in our chunks
