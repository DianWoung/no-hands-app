from pydantic import BaseModel
from typing import Optional, Dict, Any

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


# --- Order Schemas ---
class OrderBase(BaseModel):
    product_id: int
    quantity: int
    status: str
    user_id: str

class Order(OrderBase):
    id: int
    product: Product # Nesting the Product schema

    class Config:
        from_attributes = True

# --- API Response Schemas ---
class StockStatus(BaseModel):
    product_name: str
    stock: int
    status: str

class OrderStatus(BaseModel):
    order_id: int
    status: str

class KnowledgeAnswer(BaseModel):
    question: str
    answer: str
    source: str