from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel
from models import OrderStatus


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock = int


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    status: OrderStatus


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    items: List[OrderItemBase] = []

    class Config:
        orm_mode = True