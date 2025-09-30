from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.order import Order
from app.schemas.order import OrderBase


class CRUDOrder(CRUDBase[Order, OrderBase, OrderBase]):
    def get_by_id(self, db: Session, *, id: int) -> Order | None:
        return super().get(db, id=id)


order = CRUDOrder(Order)