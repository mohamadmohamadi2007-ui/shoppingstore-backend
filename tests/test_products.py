from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product():
    response = client.post("/products", json={"name": "Test Item", "price": 9.99})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"

def test_get_nonexistent_product_404():
    response = client.delete("/products/999999")
    assert response.status_code == 404

def test_pagination_limit():
    response = client.get("/products?limit=1")
    assert len(response.json()) == 1