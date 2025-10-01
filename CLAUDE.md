# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered e-commerce shopping assistant built with FastAPI backend and React frontend. The system uses LangChain/LangGraph for conversational AI with tool-calling capabilities, ChromaDB for knowledge base, and WebSocket for real-time chat.

## Development Commands

### Docker (Recommended)
```bash
# Build and run all services
docker-compose up --build

# Pull Ollama embedding model (if using local embeddings)
docker exec -it ollama ollama pull nomic-embed-text
```

### Manual Development
```bash
# Backend setup
pip install -r backend/requirements.txt

# Build knowledge base (requires OPENAI_API_KEY)
python -m backend.build_vector_store

# Run backend server
PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Frontend setup (in separate terminal)
cd frontend
npm install
npm start
```

### Frontend Commands
```bash
npm start        # Start development server
npm build        # Build for production
npm test         # Run tests
```

## Architecture

### Backend Structure
- **FastAPI Application**: `backend/app/main.py` - Main entry point with lifespan management
- **API Routes**: `backend/app/api/` - REST endpoints for products, orders, knowledge, and WebSocket chat
- **AI Agent**: `backend/app/services/agent_graph.py` - LangGraph-based conversational agent with tool calling
- **Tools**: `backend/app/services/agent_tools.py` - Database and knowledge base query tools
- **Database**: SQLAlchemy ORM with SQLite (switchable to PostgreSQL/MySQL)
- **Knowledge Base**: ChromaDB vector store for product information

### Frontend Structure
- **React App**: `frontend/src/pages/App.js` - WebSocket-based chat interface with streaming
- **Styling**: TailwindCSS for modern UI
- **Real-time**: WebSocket connection to `/api/chat/ws` endpoint

### Key Components

#### AI Agent System
- Uses LangGraph StateGraph for conversation management
- Tools for stock status, order tracking, and knowledge base queries
- OpenAI API for language model (configurable to use Ollama)
- Streaming responses via WebSocket

#### Database Models
- Products: inventory, pricing, specifications
- Orders: order tracking and status
- SQLite with automatic initialization

#### Knowledge Base
- ChromaDB vector store built from product data
- RAG (Retrieval-Augmented Generation) for product questions
- Built via `backend/app/scripts/build_vector_store.py`

## Configuration

### Environment Variables
Required in `.env` file (copy from `.env.example`):
- `OPENAI_API_KEY` - Required for AI functionality
- `EMBEDDINGS_PROVIDER` - "openai" (default) or "ollama"
- `OPENAI_MODEL_NAME` - Model for chat (default: gpt-4o)
- `OLLAMA_BASE_URL` - For local Ollama deployment

### Docker Configuration
- Backend runs on port 8000
- Frontend serves on port 3000 via Nginx
- Volumes for persistent data storage

## API Endpoints

### REST Endpoints
- `GET /api/products/{product_name}/stock` - Check product availability
- `GET /api/orders/{order_id}/status` - Check order status
- `GET /api/knowledge/search` - Search knowledge base

### WebSocket
- `ws://localhost:8000/api/chat/ws` - Real-time chat with streaming responses

## Development Notes

- Backend requires `PYTHONPATH=.` when running manually for proper imports
- Knowledge base must be built before first use
- WebSocket handles streaming AI responses with status updates
- Agent tools make HTTP requests back to the FastAPI endpoints
- Frontend auto-reconnects on WebSocket disconnect