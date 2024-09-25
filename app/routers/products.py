from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db

router = APIRouter()


@router.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.get("/products/", response_model=List[schemas.ProductResponse])
def get_products(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_products(db, offset, limit)


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.read_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_product


@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_product


@router.delete("/products/{product_id}", response_model=schemas.ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_product


