# AI Research Agent

A full-stack AI research agent that autonomously answers questions using RAG, vector embeddings, web search, and tool use. Built from scratch to demonstrate end-to-end AI engineering.

## Architecture

```
User Question
      ↓
Angular Frontend (localhost:4200)
      ↓ HTTP / SSE Stream
FastAPI Backend (localhost:8000)
      ↓
LangChain Agent (ReAct pattern)
      ↓ decides which tools to use
┌─────────────────────────────────┐
│  search_knowledge_base          │  → Voyage embeddings + cosine similarity
│  web_search                     │  → Tavily real-time internet search
│  calculate                      │  → Python eval()
└─────────────────────────────────┘
      ↓
Anthropic Claude (claude-sonnet-4-5)
      ↓ streaming tokens
Angular UI renders response in real time
```

## Stack

| Layer | Technology |
|---|---|
| LLM | Anthropic Claude (claude-sonnet-4-5) |
| Embeddings | Voyage AI (voyage-3-lite) |
| Agent Framework | LangChain |
| Web Search | Tavily |
| Backend | FastAPI + Python |
| Frontend | Angular |
| Containerization | Docker |

## Features

- **RAG Pipeline** — documents embedded into 512-dimension vectors, retrieved via cosine similarity search
- **Autonomous Agent** — ReAct pattern, decides which tools to use and in what order without being told
- **Real-time Streaming** — tokens stream from Claude → FastAPI → Angular via Server-Sent Events
- **Web Search** — Tavily integration for real-time internet search beyond the knowledge base
- **REST API** — FastAPI backend with auto-generated interactive docs at `/docs`
- **Dockerized** — runs in one command with Docker

## Project Structure

```
ai-research-agent/
├── phase1/          # LLM fundamentals (API calls, streaming, conversation)
├── phase2/          # RAG pipeline (embeddings, vector search, cosine similarity)
├── phase3/          # Agent with tool use (LangChain, ReAct pattern)
├── phase4/          # FastAPI backend (REST API, SSE streaming)
│   └── main.py
├── frontend/        # Angular frontend
│   └── src/app/
│       ├── app.component.ts
│       ├── app.component.html
│       └── research.service.ts
├── Dockerfile
├── docker-compose.yml
└── requirement.txt
```

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker 

### API Keys Required
- [Anthropic](https://console.anthropic.com) — LLM
- [Voyage AI](https://voyageai.com) — Embeddings
- [Tavily](https://tavily.com) — Web search

### Setup

```bash
git clone https://github.com/Shayannafees/ai-research-agent
cd ai-research-agent
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
cp .env.example .env
```

### Run the backend

```bash
cd phase4
uvicorn main:app --reload
```

API at `http://localhost:8000`
Docs at `http://localhost:8000/docs`

### Run the frontend

```bash
cd frontend
npm install
ng serve
```

Frontend at `http://localhost:4200`

### Run with Docker

```bash
docker-compose up
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/ask` | POST | Ask a question, get full response |
| `/ask/stream` | POST | Stream tokens in real time |

### Example

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## How It Works

### RAG Pipeline
Documents are embedded into 512-dimension vectors using Voyage AI. When a question arrives it is embedded into the same space and compared against all document vectors using cosine similarity. The top matching chunks are injected into the prompt as context.

### Agent Loop (ReAct Pattern)
1. Claude reads the question and tool descriptions
2. Decides which tools to call and with what inputs
3. AgentExecutor calls the tools and feeds results back
4. Claude reads results and decides next step or produces final answer

### Streaming
FastAPI streams tokens from Claude using Server-Sent Events. Angular reads the stream with the browser's native fetch API and appends each token to the UI as it arrives.

## Roadmap

- [ ] Authentication — JWT-based user auth
- [ ] Conversation history — multi-turn memory per user
- [ ] Document upload — let users upload their own PDFs
- [ ] Pinecone integration — production-grade vector database
- [ ] Deploy to cloud — public live URL
- [ ] Rate limiting — protect the API endpoints
- [ ] LangGraph — upgrade agent to stateful graph-based architecture
- [ ] Evaluation — measure answer quality with RAGAS

## Built In Public

Follow the build on X: [@shayannafees](https://X.com/sh_ayan7)

## Author

**Muhammad Shayan Nafees**
- ICPC Top 5 California 2025
- Full-stack engineer + AI engineering
- [GitHub](https://github.com/Shayannafees) · [X](https://X.com/sh_ayan7)
