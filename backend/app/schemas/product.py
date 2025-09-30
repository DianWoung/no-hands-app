from typing import Optional, Dict, Any
from pydantic import BaseModel

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

# --- API Response Schemas ---
class StockStatus(BaseModel):
    product_name: str
    stock: int
    status: str