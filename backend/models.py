from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, index=True)
    # Using JSON for flexible key-value specifications (e.g., color, size)
    specs = Column(JSON)

    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    # In a real system, this would link to a User model
    user_id = Column(String, index=True, default="user123")
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    status = Column(String, default="Pending") # e.g., Pending, Shipped, Delivered
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="orders")