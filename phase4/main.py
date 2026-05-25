import os
import json
import numpy as np
import voyageai
import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── CLIENTS ───────────────────────────────────────────────────────
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
voyage_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
llm = ChatAnthropic(model="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── FASTAPI APP ───────────────────────────────────────────────────
app = FastAPI(title="AI Research Agent API")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── KNOWLEDGE BASE ────────────────────────────────────────────────
documents = [
    "RAG stands for Retrieval-Augmented Generation. It combines search with LLMs to answer questions grounded in real documents.",
    "Vector databases store embeddings which are numerical representations of text meaning. Similar texts have similar embeddings.",
    "Embeddings are arrays of floating point numbers. A sentence becomes a vector like [0.2, 0.8, 0.1, ...].",
    "LangChain is a framework that simplifies building LLM applications with tools for agents, memory, and retrieval.",
    "FastAPI is a modern Python web framework for building APIs. It is async-friendly and auto-generates documentation.",
    "Agents are AI systems that can reason about which tools to use and execute them in a loop until a goal is complete.",
    "Cosine similarity measures how similar two vectors are. A score of 1 means identical, 0 means unrelated, -1 means opposite.",
]

print("Initializing knowledge base...")
result = voyage_client.embed(documents, model="voyage-3-lite")
doc_embeddings = np.array(result.embeddings)
print(f"Knowledge base ready: {len(documents)} documents")

# ── COSINE SIMILARITY ─────────────────────────────────────────────
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ── TOOLS ─────────────────────────────────────────────────────────
@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information about AI, ML, RAG,
    LangChain, FastAPI, embeddings, agents, or vector databases."""
    query_result = voyage_client.embed([query], model="voyage-3-lite")
    query_embedding = np.array(query_result.embeddings[0])
    similarities = []
    for i, doc_embedding in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_embedding)
        similarities.append((score, documents[i]))
    similarities.sort(reverse=True)
    top_docs = similarities[:2]
    return "\n".join([f"[score: {score:.3f}] {doc}" for score, doc in top_docs])

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression. Use this for any math or numbers."""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# ── AGENT SETUP ───────────────────────────────────────────────────
tools = [search_knowledge_base, calculate]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a research assistant with access to a knowledge base and calculator.
Always search the knowledge base before answering factual questions.
Think step by step about what tools you need."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ── REQUEST MODEL ─────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str

# ── ENDPOINTS ─────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "documents": len(documents)}

@app.post("/ask")
def ask(request: QuestionRequest):
    result = agent_executor.invoke({"input": request.question})
    output = result["output"]
    if isinstance(output, list):
        output = output[0].get("text", str(output))
    return {"question": request.question, "answer": output}

@app.post("/ask/stream")
def ask_stream(request: QuestionRequest):
    def generate():
        with anthropic_client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="""You are a research assistant. Answer clearly and concisely.""",
            messages=[{"role": "user", "content": request.question}]
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'token': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
