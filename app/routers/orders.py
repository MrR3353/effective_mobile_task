from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db
from app.models import OrderStatus
from app.schemas import OrderResponse, OrderItemResponse, OrderItemBase, OrderBase

router = APIRouter()


@router.post("/", response_model=OrderResponse)
def create_order(order: schemas.OrderBase, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@router.get("/", response_model=List[OrderResponse])
def get_orders(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_orders(db, offset, limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order_db = crud.read_order(db, order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order_db


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status: OrderStatus, db: Session = Depends(get_db)):
    order_db = crud.update_order_status(db, order_id, status)
    if order_db is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order_db


@router.post("/{order_id}/items", response_model=OrderItemResponse)
def add_item_to_order(order_id: int, order_item: OrderItemBase, db: Session = Depends(get_db)):
    try:
        if order_id != order_item.order_id:
            raise ValueError("Разные order_id")
        db_order_item = crud.add_order_item(db, order_item)
        return db_order_item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))