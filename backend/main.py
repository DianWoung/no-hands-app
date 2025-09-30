import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage

from . import models, schemas, crud
from .database import engine, get_db
from .knowledge_service import KnowledgeService
from .agent_graph import agent_graph

# Create database tables
models.Base.metadata.create_all(bind=engine)

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

    yield

    print("--- Application shutting down... ---")


app = FastAPI(
    title="AI E-commerce Shopping Assistant API",
    description="API endpoints for the AI Shopping Assistant, including database access and knowledge base queries.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok"}


# --- Database Tools ---

@app.get("/api/products/{product_name}/stock", response_model=schemas.StockStatus, tags=["Database Tools"])
def get_stock_status(product_name: str, db: Session = Depends(get_db)):
    """
    Retrieves the stock quantity for a given product name.
    This is a tool the AI Agent can use.
    """
    db_product = crud.get_product_by_name(db, name=product_name)
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product '{product_name}' not found")

    status = "In Stock" if db_product.stock > 0 else "Out of Stock"
    return schemas.StockStatus(product_name=db_product.name, stock=db_product.stock, status=status)


@app.get("/api/orders/{order_id}/status", response_model=schemas.OrderStatus, tags=["Database Tools"])
def get_order_status(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the shipping status for a given order ID.
    This is a tool the AI Agent can use.
    """
    db_order = crud.get_order_by_id(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail=f"Order ID '{order_id}' not found")

    return schemas.OrderStatus(order_id=db_order.id, status=db_order.status)


# --- Knowledge Base Tools ---

class QuestionRequest(schemas.BaseModel):
    question: str

@app.post("/api/knowledge/answer", response_model=schemas.KnowledgeAnswer, tags=["Knowledge Base Tools"])
def get_knowledge_answer(req: Request, request_data: QuestionRequest):
    """
    Answers a question by searching the knowledge base.
    This is a tool the AI Agent can use.
    """
    knowledge_service = req.app.state.knowledge_service
    if knowledge_service is None:
        raise HTTPException(
            status_code=503,
            detail="KnowledgeService is not available. Ensure OPENAI_API_KEY is set and vector store is built."
        )

    result = knowledge_service.answer_question(request_data.question)
    return schemas.KnowledgeAnswer(
        question=request_data.question,
        answer=result["answer"],
        source=result["source"]
    )

from langchain_core.messages import AIMessage

# --- Chat WebSocket Endpoint ---

@app.websocket("/api/chat/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handles the WebSocket connection for the chat interface.
    Streams the agent's intermediate steps and final answer token by token.
    """
    await websocket.accept()
    # Each connection gets its own conversation history.
    # In a real app, you'd tie this to user sessions.
    history = []
    try:
        while True:
            user_message = await websocket.receive_text()

            # Add user message to history
            history.append(HumanMessage(content=user_message))
            graph_input = {"messages": history}

            full_response = ""

            # Use astream_events to get token-level streaming
            async for event in agent_graph.astream_events(graph_input, version="v1"):
                kind = event["event"]

                if kind == "on_tool_start":
                    await websocket.send_json({
                        "type": "status",
                        "content": f"Calling tool: `{event['name']}`..."
                    })

                elif kind == "on_tool_end":
                    # This provides the output of the tool
                    await websocket.send_json({
                        "type": "status",
                        "content": f"Tool `{event['name']}` finished. Analyzing results..."
                    })

                elif kind == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]
                    if isinstance(chunk, AIMessage) and chunk.content:
                        full_response += chunk.content
                        await websocket.send_json({
                            "type": "stream_chunk",
                            "content": chunk.content
                        })

            # The full response is now assembled, add it to the history
            history.append(AIMessage(content=full_response))
            await websocket.send_json({"type": "stream_end"})

    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")