from sqlmodel import Session, select
from app.schemas import Variant, VariantCreate, VariantUpdate
from datetime import datetime, timezone


def list_variants(session: Session, product_id: int | None, skip: int, limit: int):
    query = select(Variant)
    if product_id is not None:
        query = query.where(Variant.product_id == product_id)
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()


def get_variant(session: Session, variant_id: int):
    return session.get(Variant, variant_id)


def create_variant(session: Session, variant: VariantCreate):
    db_variant = Variant.model_validate(variant)
    session.add(db_variant)
    session.commit()
    session.refresh(db_variant)
    return db_variant


def update_variant(session: Session, variant_id: int, variant: VariantUpdate):
    db_variant = session.get(Variant, variant_id)
    if not db_variant:
        return None
    db_variant.color = variant.color
    db_variant.price_override = variant.price_override
    db_variant.stock_qty = variant.stock_qty
    db_variant.updated_at = datetime.now(timezone.utc)
    session.add(db_variant)
    session.commit()
    session.refresh(db_variant)
    return db_variant


def delete_variant(session: Session, variant_id: int) -> bool:
    db_variant = session.get(Variant, variant_id)
    if not db_variant:
        return False
    session.delete(db_variant)
    session.commit()
    return True