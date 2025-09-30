from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{order_id}/status", response_model=schemas.OrderStatus)
def get_order_status(
    order_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Retrieves the shipping status for a given order ID.
    """
    db_order = crud.order.get_by_id(db, id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail=f"Order ID '{order_id}' not found")

    return schemas.OrderStatus(order_id=db_order.id, status=db_order.status)