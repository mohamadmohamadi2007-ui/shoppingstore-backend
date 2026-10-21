from fastapi import FastAPI, HTTPException
from app.schemas import Product

app = FastAPI(title="ShoppingStore Backend")

PRODUCTS = [
    {"id": 1, "name": "T-Shirt", "price": 19.99},
    {"id": 2, "name": "Jeans", "price": 49.99},
]

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/hello_world")
def health() -> dict[str, str]:
    return {
        "message": "Hello Mohammad"
        }

@app.get("/version")
def version():
    return {"version": "0.1.0"}

@app.get("/products", response_model=list[Product])
def get_products():
    return PRODUCTS

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")
