from pydantic import BaseModel
from .product import Product

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
class OrderStatus(BaseModel):
    order_id: int
    status: str