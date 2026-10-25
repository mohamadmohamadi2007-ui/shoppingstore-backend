from fastapi import FastAPI
from app.database import engine, create_db_and_tables
from app.api.products import router as products_router
from app.api.variants import router as variants_router
from app.api.carts import router as carts_router
from app.api.orders import router as orders_router
from app.schemas import Product, Category, Variant
from sqlmodel import Session, select

app = FastAPI(title="ShoppingStore Backend")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Category)).first():
            session.add(Category(name="Bras", slug="bras"))
            session.add(Category(name="Panties", slug="panties"))
            session.commit()
        if not session.exec(select(Product)).first():
            session.add(Product(
                product_code="BRA001", 
                name="Classic Push-up Bra",
                category_id=1,
                base_price=890000))
            session.add(Product(
                product_code="BRA002", 
                name="Everyday Wireless Bra",
                category_id=1,
                base_price=750000))
            session.commit()
        if not session.exec(select(Variant)).first():
            session.add(Variant(
                product_id=1, 
                sku="BRA001-34B-BLK", 
                band="34", 
                cup="B", 
                color="Black", 
                stock_qty=10))
            session.add(Variant(
                product_id=1, 
                sku="BRA001-34B-WHT", 
                band="34", 
                cup="B", 
                color="White", 
                stock_qty=5))
            session.commit()


app.include_router(products_router)
app.include_router(variants_router)
app.include_router(carts_router)
app.include_router(orders_router)