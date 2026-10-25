from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.schemas import ProductImage, ProductImageCreate
from app.database import get_session
from app.services import image_service

router = APIRouter()


@router.post("/products/{product_id}/images", response_model=ProductImage, status_code=201)
def create_image(product_id: int, image: ProductImageCreate, session: Session = Depends(get_session)):
    db_image = image_service.create_image(session, product_id, image)
    if not db_image:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_image


@router.get("/products/{product_id}/images", response_model=list[ProductImage])
def list_images(product_id: int, session: Session = Depends(get_session)):
    return image_service.list_images(session, product_id)


@router.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: int, session: Session = Depends(get_session)):
    deleted = image_service.delete_image(session, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")
