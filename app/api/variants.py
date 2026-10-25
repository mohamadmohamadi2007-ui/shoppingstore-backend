from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.schemas import Variant, VariantCreate, VariantUpdate
from app.database import get_session
from app.services import variant_service

router = APIRouter()


@router.get("/variants", response_model=list[Variant])
def list_variants(
    product_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    return variant_service.list_variants(session, product_id, skip, limit)


@router.get("/variants/{variant_id}", response_model=Variant)
def get_variant(variant_id: int, session: Session = Depends(get_session)):
    variant = variant_service.get_variant(session, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant


@router.post("/variants", response_model=Variant, status_code=201)
def create_variant(variant: VariantCreate, session: Session = Depends(get_session)):
    return variant_service.create_variant(session, variant)


@router.put("/variants/{variant_id}", response_model=Variant)
def update_variant(variant_id: int, variant: VariantUpdate, session: Session = Depends(get_session)):
    db_variant = variant_service.update_variant(session, variant_id, variant)
    if not db_variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return db_variant


@router.delete("/variants/{variant_id}", status_code=204)
def delete_variant(variant_id: int, session: Session = Depends(get_session)):
    deleted = variant_service.delete_variant(session, variant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Variant not found")