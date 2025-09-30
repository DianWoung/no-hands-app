from sqlalchemy.orm import Session
from . import models, schemas

# --- Product CRUD Operations ---

def get_product_by_name(db: Session, name: str) -> models.Product | None:
    """
    Retrieves the first product found with the given name.
    Note: In a real system, you might want a more robust lookup (e.g., by SKU).
    """
    return db.query(models.Product).filter(models.Product.name.ilike(f"%{name}%")).first()

# --- Order CRUD Operations ---

def get_order_by_id(db: Session, order_id: int) -> models.Order | None:
    """
    Retrieves an order by its primary key.
    """
    return db.query(models.Order).filter(models.Order.id == order_id).first()