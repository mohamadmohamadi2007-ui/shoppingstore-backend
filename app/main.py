from fastapi import FastAPI
from app.database import engine, create_db_and_tables
from app.api.products import router as products_router
from app.schemas import Product
from sqlmodel import Session, select

app = FastAPI(title="ShoppingStore Backend")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Product)).first():
            session.add(Product(name="T-Shirt", price=19.99))
            session.add(Product(name="Jeans", price=49.99))
            session.commit()


app.include_router(products_router)