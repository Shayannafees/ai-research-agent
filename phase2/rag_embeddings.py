import os
import numpy as np
import voyageai
import anthropic
from dotenv import load_dotenv

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

# ── 1. OUR DOCUMENT CHUNKS ────────────────────────────────────────
chunks = [
    "RAG stands for Retrieval-Augmented Generation. It combines search with LLMs to answer questions grounded in real documents.",
    "Vector databases store embeddings which are numerical representations of text meaning. Similar texts have similar embeddings.",
    "Embeddings are arrays of floating point numbers. A sentence becomes a vector like [0.2, 0.8, 0.1, ...].",
    "LangChain is a framework that simplifies building LLM applications with tools for agents, memory, and retrieval.",
    "FastAPI is a modern Python web framework for building APIs. It is async-friendly and auto-generates documentation.",
]

# ── 2. EMBED ALL CHUNKS ───────────────────────────────────────────
print("Embedding chunks...")
result = voyage_client.embed(chunks, model="voyage-3-lite")
chunk_embeddings = np.array(result.embeddings)
print(f"Each embedding has {chunk_embeddings.shape[1]} dimensions")
print(f"Total chunks embedded: {chunk_embeddings.shape[0]}\n")

# ── 3. COSINE SIMILARITY ──────────────────────────────────────────
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ── 4. FIND RELEVANT CHUNKS ───────────────────────────────────────
def find_relevant_chunks(query, top_k=2):
    # embed the query using the same model
    query_result = voyage_client.embed([query], model="voyage-3-lite")
    query_embedding = np.array(query_result.embeddings[0])

    # compare query vector against every chunk vector
    similarities = []
    for i, chunk_embedding in enumerate(chunk_embeddings):
        score = cosine_similarity(query_embedding, chunk_embedding)
        similarities.append((score, i, chunks[i]))

    # sort by score descending, return top_k
    similarities.sort(reverse=True)
    return similarities[:top_k]

# ── 5. RAG PIPELINE ───────────────────────────────────────────────
def ask(question):
    print(f"Question: {question}")

    # retrieve
    relevant = find_relevant_chunks(question)
    print("Relevant chunks found:")
    for score, i, chunk in relevant:
        print(f"  [{score:.3f}] {chunk[:60]}...")

    # build context
    context = "\n".join([chunk for score, i, chunk in relevant])

    # generate
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        system="""You are a research assistant. Answer questions using ONLY
the provided context. If the answer is not in the context, say so.""",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )

    print(f"\nAnswer: {response.content[0].text}\n")
    print("-" * 50 + "\n")

# ── 6. TEST ───────────────────────────────────────────────────────
ask("What is RAG and how does it work?")
ask("What is FastAPI used for?")
ask("What is the capital of France?")
