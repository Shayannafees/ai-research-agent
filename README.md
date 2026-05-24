# AI Research Agent

A full-stack AI agent that autonomously researches topics using RAG, embeddings, and tool use.

Built in public — learning AI engineering from scratch.

## Stack
Anthropic API · Voyage Embeddings · LangChain · FastAPI · Angular · Docker

## Phases
- [x] Phase 1 — LLM Foundations (API calls, streaming, conversation history)
- [x] Phase 2 — RAG & Embeddings (vector search, cosine similarity)
- [ ] Phase 3 — Agents & Tool Use
- [ ] Phase 4 — FastAPI Backend
- [ ] Phase 5 — Angular Frontend

## Phase 1 — LLM Foundations
Learned how to make basic API calls, use system prompts to control model output,
stream responses token by token, and manage multi-turn conversation history.

## Phase 2 — RAG & Embeddings
Built a retrieval-augmented generation pipeline from scratch. Documents are split
into chunks, embedded into 512-dimension vectors using Voyage AI, and retrieved
via cosine similarity search. Only relevant chunks are injected into the prompt.
