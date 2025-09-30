from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{product_name}/stock", response_model=schemas.StockStatus)
def get_stock_status(
    product_name: str,
    db: Session = Depends(deps.get_db),
):
    """
    Retrieves the stock quantity for a given product name.
    """
    db_product = crud.product.get_by_name(db, name=product_name)
    if db_product is None:
        raise HTTPException(
            status_code=404, detail=f"Product '{product_name}' not found"
        )

    status = "In Stock" if db_product.stock > 0 else "Out of Stock"
    return schemas.StockStatus(
        product_name=db_product.name, stock=db_product.stock, status=status
    )