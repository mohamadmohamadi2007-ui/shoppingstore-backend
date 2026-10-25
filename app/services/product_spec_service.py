from sqlmodel import Session, select
from app.schemas import Product, ProductSpec, ProductSpecCreate


def create_spec(session: Session, product_id: int, spec: ProductSpecCreate):
    if not session.get(Product, product_id):
        return None
    db_spec = ProductSpec(product_id=product_id, **spec.model_dump())
    session.add(db_spec)
    session.commit()
    session.refresh(db_spec)
    return db_spec


def get_spec(session: Session, product_id: int):
    return session.exec(select(ProductSpec).where(ProductSpec.product_id == product_id)).first()


def delete_spec(session: Session, product_id: int) -> bool:
    db_spec = session.exec(select(ProductSpec).where(ProductSpec.product_id == product_id)).first()
    if not db_spec:
        return False
    session.delete(db_spec)
    session.commit()
    return True
