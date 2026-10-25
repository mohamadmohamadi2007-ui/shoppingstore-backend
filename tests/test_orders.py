import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.main import app
from app.database import engine
from app.schemas import Cart, CartItem, Order, OrderItem


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_checkout_creates_order_and_decrements_stock(client):
    variant_resp = client.post("/variants", json={
        "product_id": 1,
        "sku": "CHECKOUT-TEST-1",
        "color": "Teal",
        "stock_qty": 5,
        "price_override": 100.0,
    })
    variant_id = variant_resp.json()["id"]

    cart_id = client.post("/carts", json={"customer_id": 1}).json()["id"]
    client.post(f"/carts/{cart_id}/items", json={"variant_id": variant_id, "qty": 2})

    response = client.post(f"/checkout/{cart_id}")
    assert response.status_code == 201
    order = response.json()
    assert order["total"] == 200.0
    assert len(order["items"]) == 1
    assert order["items"][0]["qty"] == 2

    assert client.get(f"/variants/{variant_id}").json()["stock_qty"] == 3

    with Session(engine) as session:
        for oi in session.exec(select(OrderItem).where(OrderItem.order_id == order["id"])).all():
            session.delete(oi)
        session.delete(session.get(Order, order["id"]))
        session.delete(session.get(Cart, cart_id))
        session.commit()
    client.delete(f"/variants/{variant_id}")


def test_checkout_insufficient_stock_returns_400(client):
    variant_resp = client.post("/variants", json={
        "product_id": 1,
        "sku": "CHECKOUT-TEST-2",
        "color": "Maroon",
        "stock_qty": 1,
    })
    variant_id = variant_resp.json()["id"]

    cart_id = client.post("/carts", json={"customer_id": 1}).json()["id"]
    client.post(f"/carts/{cart_id}/items", json={"variant_id": variant_id, "qty": 5})

    response = client.post(f"/checkout/{cart_id}")
    assert response.status_code == 400

    with Session(engine) as session:
        for ci in session.exec(select(CartItem).where(CartItem.cart_id == cart_id)).all():
            session.delete(ci)
        session.delete(session.get(Cart, cart_id))
        session.commit()
    client.delete(f"/variants/{variant_id}")