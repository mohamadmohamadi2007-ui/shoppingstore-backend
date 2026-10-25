import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def product(client):
    response = client.post("/products", json={
        "product_code": "SPECTEST1",
        "name": "Spec Test Product",
        "category_id": 1,
        "base_price": 100000,
    })
    product_id = response.json()["id"]
    yield product_id
    client.delete(f"/products/{product_id}")


def test_create_and_get_spec(client, product):
    response = client.post(f"/products/{product}/spec", json={
        "fabric": "Cotton",
        "care_instructions": "Machine wash cold",
        "origin_country": "Iran",
    })
    assert response.status_code == 201
    assert response.json()["fabric"] == "Cotton"

    get_response = client.get(f"/products/{product}/spec")
    assert get_response.status_code == 200
    assert get_response.json()["origin_country"] == "Iran"

    client.delete(f"/products/{product}/spec")


def test_create_spec_for_nonexistent_product_404(client):
    response = client.post("/products/999999/spec", json={
        "fabric": "Cotton",
        "care_instructions": "Machine wash cold",
        "origin_country": "Iran",
    })
    assert response.status_code == 404


def test_get_nonexistent_spec_404(client, product):
    response = client.get(f"/products/{product}/spec")
    assert response.status_code == 404


def test_delete_spec(client, product):
    client.post(f"/products/{product}/spec", json={
        "fabric": "Silk",
        "care_instructions": "Hand wash only",
        "origin_country": "Italy",
    })
    delete_response = client.delete(f"/products/{product}/spec")
    assert delete_response.status_code == 204
    assert client.get(f"/products/{product}/spec").status_code == 404
