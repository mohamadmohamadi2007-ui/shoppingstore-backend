import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.main import app
from app.database import engine
from app.schemas import Customer


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _cleanup_customer(phone_number: str):
    with Session(engine) as session:
        customer = session.exec(
            select(Customer).where(Customer.phone_number == phone_number)
        ).first()
        if customer:
            session.delete(customer)
            session.commit()


def test_request_otp_creates_customer_and_returns_debug_code(client):
    phone_number = "09121110001"
    response = client.post("/auth/otp/request", json={"phone_number": phone_number})
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "OTP sent"
    assert "debug_otp" in body
    assert len(body["debug_otp"]) == 6

    with Session(engine) as session:
        customer = session.exec(
            select(Customer).where(Customer.phone_number == phone_number)
        ).first()
        assert customer is not None
        assert customer.otp_code_hash is not None

    _cleanup_customer(phone_number)


def test_verify_otp_returns_access_token_and_grants_me(client):
    phone_number = "09121110002"
    otp_code = client.post("/auth/otp/request", json={"phone_number": phone_number}).json()["debug_otp"]

    response = client.post("/auth/otp/verify", json={"phone_number": phone_number, "otp_code": otp_code})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["phone_number"] == phone_number

    _cleanup_customer(phone_number)


def test_verify_otp_wrong_code_returns_400(client):
    phone_number = "09121110003"
    client.post("/auth/otp/request", json={"phone_number": phone_number})

    response = client.post("/auth/otp/verify", json={"phone_number": phone_number, "otp_code": "000000"})
    assert response.status_code == 400

    _cleanup_customer(phone_number)


def test_verify_otp_expired_returns_400(client):
    phone_number = "09121110004"
    otp_code = client.post("/auth/otp/request", json={"phone_number": phone_number}).json()["debug_otp"]

    from datetime import datetime, timedelta, timezone
    with Session(engine) as session:
        customer = session.exec(
            select(Customer).where(Customer.phone_number == phone_number)
        ).first()
        customer.otp_expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        session.add(customer)
        session.commit()

    response = client.post("/auth/otp/verify", json={"phone_number": phone_number, "otp_code": otp_code})
    assert response.status_code == 400

    _cleanup_customer(phone_number)


def test_me_without_token_returns_401(client):
    response = client.get("/auth/me")
    assert response.status_code in (401, 403)


def test_me_with_invalid_token_returns_401(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401
