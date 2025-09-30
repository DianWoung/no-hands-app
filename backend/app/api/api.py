from fastapi import APIRouter

from app.api.endpoints import products, orders, knowledge, chat

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["Database Tools"])
api_router.include_router(orders.router, prefix="/orders", tags=["Database Tools"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Base Tools"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])