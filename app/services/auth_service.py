from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.schemas import Customer
from app.security import generate_otp_code, hash_otp_code, verify_otp_code

OTP_TTL_MINUTES = 5


def request_otp(session: Session, phone_number: str) -> tuple[Customer, str]:
    customer = session.exec(
        select(Customer).where(Customer.phone_number == phone_number)
    ).first()
    if not customer:
        customer = Customer(phone_number=phone_number)

    otp_code = generate_otp_code()
    customer.otp_code_hash = hash_otp_code(otp_code)
    customer.otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_TTL_MINUTES)
    customer.updated_at = datetime.now(timezone.utc)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer, otp_code


def verify_otp(session: Session, phone_number: str, otp_code: str) -> Customer:
    customer = session.exec(
        select(Customer).where(Customer.phone_number == phone_number)
    ).first()
    if not customer or not customer.otp_code_hash or not customer.otp_expires_at:
        raise ValueError("OTP not requested for this phone number")

    if datetime.now(timezone.utc) > customer.otp_expires_at:
        raise ValueError("OTP expired")

    if not verify_otp_code(otp_code, customer.otp_code_hash):
        raise ValueError("invalid OTP")

    customer.otp_code_hash = None
    customer.otp_expires_at = None
    customer.is_active = True
    customer.updated_at = datetime.now(timezone.utc)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
