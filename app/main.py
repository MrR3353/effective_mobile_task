from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import products, orders

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products.router, prefix='/products', tags=["products"])
app.include_router(orders.router, prefix='/orders', tags=["orders"])