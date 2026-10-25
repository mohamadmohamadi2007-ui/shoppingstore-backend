import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_list_variants(client):
    response = client.get("/variants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_variant(client):
    response = client.post("/variants", json={
        "product_id": 1,
        "sku": "TESTVAR1",
        "color": "Red",
        "stock_qty": 3,
    })
    assert response.status_code == 201
    assert response.json()["color"] == "Red"
    client.delete(f"/variants/{response.json()['id']}")


def test_get_nonexistent_variant_404(client):
    response = client.get("/variants/999999")
    assert response.status_code == 404


def test_update_variant(client):
    create = client.post("/variants", json={
        "product_id": 1,
        "sku": "TESTVAR2",
        "color": "Blue",
        "stock_qty": 1,
    })
    variant_id = create.json()["id"]
    response = client.put(f"/variants/{variant_id}", json={"color": "Green", "stock_qty": 2})
    assert response.status_code == 200
    assert response.json()["color"] == "Green"
    client.delete(f"/variants/{variant_id}")