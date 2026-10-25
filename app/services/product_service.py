from sqlmodel import Session, select
from app.schemas import Product, ProductCreate, ProductUpdate
from datetime import datetime, timezone


def list_products(session: Session, min_price: float | None, max_price: float | None, name: str | None, skip: int, limit: int):
    query = select(Product)
    if min_price is not None:
        query = query.where(Product.base_price >= min_price)
    if max_price is not None:
        query = query.where(Product.base_price <= max_price)
    if name is not None:
        query = query.where(Product.name.contains(name))
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()


def get_product(session: Session, product_id: int):
    return session.get(Product, product_id)


def create_product(session: Session, product: ProductCreate):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def update_product(session: Session, product_id: int, product: ProductUpdate):
    db_product = session.get(Product, product_id)
    if not db_product:
        return None
    db_product.name = product.name
    db_product.base_price = product.base_price
    db_product.updated_at = datetime.now(timezone.utc)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def delete_product(session: Session, product_id: int) -> bool:
    db_product = session.get(Product, product_id)
    if not db_product:
        return False
    session.delete(db_product)
    session.commit()
    return True