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
        "product_code": "IMGTEST1",
        "name": "Image Test Product",
        "category_id": 1,
        "base_price": 100000,
    })
    product_id = response.json()["id"]
    yield product_id
    client.delete(f"/products/{product_id}")


def test_create_and_list_images(client, product):
    response = client.post(f"/products/{product}/images", json={
        "url": "/static/images/products/product-lace-black.png",
        "sort_order": 0,
        "is_primary": True,
    })
    assert response.status_code == 201
    assert response.json()["is_primary"] is True

    list_response = client.get(f"/products/{product}/images")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    client.delete(f"/images/{response.json()['id']}")


def test_create_image_for_nonexistent_product_404(client):
    response = client.post("/products/999999/images", json={
        "url": "/static/images/products/product-bridal-lace.png",
    })
    assert response.status_code == 404


def test_delete_image(client, product):
    create = client.post(f"/products/{product}/images", json={
        "url": "/static/images/products/product-satin-rosegold.png",
    })
    image_id = create.json()["id"]
    delete_response = client.delete(f"/images/{image_id}")
    assert delete_response.status_code == 204
    assert client.get(f"/products/{product}/images").json() == []


def test_delete_nonexistent_image_404(client):
    response = client.delete("/images/999999")
    assert response.status_code == 404
