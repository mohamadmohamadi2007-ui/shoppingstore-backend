from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_list_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product(client):
    response = client.post("/products", json={"product_code": "TEST", "name": "Test Item", "base_price": 9.99, "category_id": 1})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
    client.delete(f"/products/{response.json()['id']}")

def test_get_nonexistent_product_404(client):
    response = client.delete("/products/999999")
    assert response.status_code == 404

def test_pagination_limit(client):
    response = client.get("/products?limit=1")
    assert len(response.json()) == 1