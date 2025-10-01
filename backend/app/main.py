import asyncio
from contextlib import asynccontextmanager
# Force reload to pick up .env changes

from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.services.knowledge_service import KnowledgeService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the FastAPI application.
    Initializes the KnowledgeService on startup.
    """
    print("--- Application starting up... ---")
    try:
        # Use asyncio.to_thread to run the synchronous KnowledgeService constructor
        # in a separate thread to avoid blocking the event loop.
        app.state.knowledge_service = await asyncio.to_thread(KnowledgeService)
        print("--- KnowledgeService initialized successfully. ---")
    except (ValueError, FileNotFoundError) as e:
        app.state.knowledge_service = None
        print(f"--- KnowledgeService initialization failed: {e} ---")
        print("--- The knowledge base API will be unavailable. ---")

    db = SessionLocal()
    init_db(db)
    yield
    db.close()
    print("--- Application shutting down... ---")


app = FastAPI(
    title="AI E-commerce Shopping Assistant API",
    description="API endpoints for the AI Shopping Assistant, including database access and knowledge base queries.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok"}


app.include_router(api_router, prefix="/api")