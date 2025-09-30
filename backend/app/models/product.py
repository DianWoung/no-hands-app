from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, index=True)
    specs = Column(JSON)

    orders = relationship("Order", back_populates="product")