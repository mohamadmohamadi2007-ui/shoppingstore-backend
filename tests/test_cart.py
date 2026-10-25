import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.main import app
from app.database import engine
from app.schemas import Cart, CartItem


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _cleanup_cart(cart_id: int):
    with Session(engine) as session:
        for item in session.exec(select(CartItem).where(CartItem.cart_id == cart_id)).all():
            session.delete(item)
        db_cart = session.get(Cart, cart_id)
        if db_cart:
            session.delete(db_cart)
        session.commit()


def test_create_cart(client):
    response = client.post("/carts", json={"customer_id": 1})
    assert response.status_code == 201
    cart = response.json()
    assert cart["customer_id"] == 1
    assert cart["items"] == []
    _cleanup_cart(cart["id"])


def test_get_cart_returns_items(client):
    variant_resp = client.post("/variants", json={
        "product_id": 1,
        "sku": "CART-TEST-1",
        "color": "Navy",
        "stock_qty": 10,
        "price_override": 50.0,
    })
    variant_id = variant_resp.json()["id"]

    cart_id = client.post("/carts", json={"customer_id": 1}).json()["id"]
    client.post(f"/carts/{cart_id}/items", json={"variant_id": variant_id, "qty": 3})

    response = client.get(f"/carts/{cart_id}")
    assert response.status_code == 200
    cart = response.json()
    assert cart["id"] == cart_id
    assert len(cart["items"]) == 1
    assert cart["items"][0]["variant_id"] == variant_id
    assert cart["items"][0]["qty"] == 3

    _cleanup_cart(cart_id)
    client.delete(f"/variants/{variant_id}")


def test_get_cart_not_found(client):
    response = client.get("/carts/999999")
    assert response.status_code == 404


def test_add_item_cart_not_found(client):
    response = client.post("/carts/999999/items", json={"variant_id": 1, "qty": 1})
    assert response.status_code == 404


def test_update_item(client):
    variant_id = client.post("/variants", json={
        "product_id": 1,
        "sku": "CART-TEST-2",
        "color": "Olive",
        "stock_qty": 10,
    }).json()["id"]

    cart_id = client.post("/carts", json={"customer_id": 1}).json()["id"]
    item = client.post(f"/carts/{cart_id}/items", json={"variant_id": variant_id, "qty": 1}).json()

    response = client.put(f"/carts/items/{item['id']}", json={"qty": 5})
    assert response.status_code == 200
    assert response.json()["qty"] == 5

    _cleanup_cart(cart_id)
    client.delete(f"/variants/{variant_id}")


def test_update_item_not_found(client):
    response = client.put("/carts/items/999999", json={"qty": 2})
    assert response.status_code == 404


def test_remove_item(client):
    variant_id = client.post("/variants", json={
        "product_id": 1,
        "sku": "CART-TEST-3",
        "color": "Rust",
        "stock_qty": 10,
    }).json()["id"]

    cart_id = client.post("/carts", json={"customer_id": 1}).json()["id"]
    item = client.post(f"/carts/{cart_id}/items", json={"variant_id": variant_id, "qty": 1}).json()

    response = client.delete(f"/carts/items/{item['id']}")
    assert response.status_code == 204

    cart = client.get(f"/carts/{cart_id}").json()
    assert cart["items"] == []

    _cleanup_cart(cart_id)
    client.delete(f"/variants/{variant_id}")


def test_remove_item_not_found(client):
    response = client.delete("/carts/items/999999")
    assert response.status_code == 404
