import os
import anthropic
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── 1. INITIALIZE THE MODEL ───────────────────────────────────────
llm = ChatAnthropic(
    model="claude-sonnet-4-5",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ── 2. DEFINE TOOLS ───────────────────────────────────────────────
# Tools are just Python functions with a @tool decorator
# The docstring is what the model reads to understand what the tool does

@tool
def search(query: str) -> str:
    """Search for information about a topic. Use this when you need
    to find facts, definitions, or current information."""
    # In a real app this would call a real search API
    # For now we simulate it with a dictionary
    knowledge = {
        "rag": "RAG stands for Retrieval-Augmented Generation. It combines search with LLMs to answer questions grounded in real documents.",
        "langchain": "LangChain is a framework for building LLM applications with tools for agents, memory, and retrieval.",
        "fastapi": "FastAPI is a modern Python web framework for building APIs. It is async-friendly and auto-generates documentation.",
        "vector database": "A vector database stores embeddings and enables similarity search across millions of vectors efficiently.",
        "embeddings": "Embeddings are numerical representations of text meaning. Similar texts have similar embeddings.",
    }
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    return f"No information found for: {query}"

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression. Use this for any math operations."""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

@tool
def summarize(text: str) -> str:
    """Summarize a long piece of text into key points."""
    sentences = text.split(".")
    key_points = [s.strip() for s in sentences if len(s.strip()) > 20]
    return "Key points:\n" + "\n".join(f"- {p}" for p in key_points[:3])

# ── 3. CREATE THE AGENT ───────────────────────────────────────────
tools = [search, calculate, summarize]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a research assistant with access to tools.
Think step by step about what tools you need to answer the question.
Always use tools to gather information before answering."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ── 4. RUN THE AGENT ──────────────────────────────────────────────
print("=" * 50)
print("Query 1: Simple search")
print("=" * 50)
result = agent_executor.invoke({
    "input": "What is RAG and what is LangChain?"
})
print(f"\nFinal Answer: {result['output']}\n")

print("=" * 50)
print("Query 2: Math + search combined")
print("=" * 50)
result = agent_executor.invoke({
    "input": "What are embeddings, and if I have 512 dimensions and 1000 documents, how many total numbers am I storing?"
})
print(f"\nFinal Answer: {result['output']}\n")
