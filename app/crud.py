from sqlalchemy.orm import Session
import models
from schemas import ProductBase, OrderBase, OrderItemBase


# PRODUCT
def read_products(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Product).offset(offset).limit(limit).all()


def read_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: ProductBase):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductBase):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


# ORDER
def read_orders(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Order).offset(offset).limit(limit).all()


def read_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def create_order(db: Session, order: OrderBase):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order_status(db: Session, order_id: int, status: models.OrderStatus):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order


# ORDER_ITEM
def add_order_item(db: Session, order_item: OrderItemBase):
    db_order_item = models.OrderItem(**order_item.dict())
    product = db.query(models.Product).filter(models.Product.id == order_item.product_id).first()
    if product and product.stock > order_item.quantity:
        product.stock -= order_item.quantity
        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)
    else:
        raise ValueError(f"Недостаточно товара на складе: {product.name} - {product.stock}")
    return db_order_item
