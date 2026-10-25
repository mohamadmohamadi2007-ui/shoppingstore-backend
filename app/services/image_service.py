from sqlmodel import Session, select
from app.schemas import Product, ProductImage, ProductImageCreate


def create_image(session: Session, product_id: int, image: ProductImageCreate):
    if not session.get(Product, product_id):
        return None
    db_image = ProductImage(product_id=product_id, **image.model_dump())
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image


def list_images(session: Session, product_id: int):
    return session.exec(select(ProductImage).where(ProductImage.product_id == product_id)).all()


def delete_image(session: Session, image_id: int) -> bool:
    db_image = session.get(ProductImage, image_id)
    if not db_image:
        return False
    session.delete(db_image)
    session.commit()
    return True
