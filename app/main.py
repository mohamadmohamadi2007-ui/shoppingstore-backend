from fastapi import FastAPI, HTTPException, Depends
from app.schemas import Product, ProductCreate
from app.database import engine, get_session, create_db_and_tables
from sqlmodel import Session, select

app = FastAPI(title="ShoppingStore Backend")

PRODUCTS = [
    {"id": 1, "name": "T-Shirt", "price": 19.99},
    {"id": 2, "name": "Jeans", "price": 49.99},
]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Product)).first():
            session.add(Product(name="T-Shirt", price=19.99))
            session.add(Product(name="Jeans", price=49.99))
            session.commit()

@app.get("/products", response_model=list[Product])
def list_products(
    min_price: float | None = None,
    max_price: float | None = None,
    name: str | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    query = select(Product)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if name is not None:
        query = query.where(Product.name.contains(name))
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate,  session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.price = product.price
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
    session.delete(db_product)
    session.commit()
    
