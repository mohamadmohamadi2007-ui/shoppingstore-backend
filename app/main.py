from fastapi import FastAPI, HTTPException
from app.schemas import Product, ProductCreate

app = FastAPI(title="ShoppingStore Backend")

PRODUCTS = [
    {"id": 1, "name": "T-Shirt", "price": 19.99},
    {"id": 2, "name": "Jeans", "price": 49.99},
]

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/products", response_model=list[Product])
def get_products():
    return PRODUCTS

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate):
    new_id = max(
        (p["id"] for p in PRODUCTS), default=0) + 1
    new_product = {"id": new_id, "name": product.name, "price": product.price}
    PRODUCTS.append(new_product)
    return new_product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate):
    for existing in PRODUCTS:
        if existing["id"] == product_id:
            existing["name"] = product.name
            existing["price"] = product.price
            return existing
    raise HTTPException(status_code=404, detail="Product not found")



@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    for i, existing in enumerate(PRODUCTS):
        if existing["id"] == product_id:
            PRODUCTS.pop(i)
            return
    raise HTTPException(status_code=404, detail="Product not found")