from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.schemas import ProductSpec, ProductSpecCreate
from app.database import get_session
from app.services import product_spec_service

router = APIRouter()


@router.post("/products/{product_id}/spec", response_model=ProductSpec, status_code=201)
def create_spec(product_id: int, spec: ProductSpecCreate, session: Session = Depends(get_session)):
    db_spec = product_spec_service.create_spec(session, product_id, spec)
    if not db_spec:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_spec


@router.get("/products/{product_id}/spec", response_model=ProductSpec)
def get_spec(product_id: int, session: Session = Depends(get_session)):
    db_spec = product_spec_service.get_spec(session, product_id)
    if not db_spec:
        raise HTTPException(status_code=404, detail="Spec not found")
    return db_spec


@router.delete("/products/{product_id}/spec", status_code=204)
def delete_spec(product_id: int, session: Session = Depends(get_session)):
    deleted = product_spec_service.delete_spec(session, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Spec not found")
