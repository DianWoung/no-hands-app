from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductBase


class CRUDProduct(CRUDBase[Product, ProductBase, ProductBase]):
    def get_by_name(self, db: Session, *, name: str) -> Product | None:
        return db.query(Product).filter(Product.name.ilike(f"%{name}%")).first()


product = CRUDProduct(Product)