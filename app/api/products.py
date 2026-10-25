from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.schemas import Product, ProductCreate, ProductUpdate
from app.database import get_session
from app.services import product_service

router = APIRouter()


@router.get("/products", response_model=list[Product])
def list_products(
    min_price: float | None = None,
    max_price: float | None = None,
    name: str | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    return product_service.list_products(session, min_price, max_price, name, skip, limit)


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = product_service.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    return product_service.create_product(session, product)


@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, session: Session = Depends(get_session)):
    db_product = product_service.update_product(session, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    deleted = product_service.delete_product(session, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")