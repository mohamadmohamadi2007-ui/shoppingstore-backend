import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


def generate_otp_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp_code(otp_code: str) -> str:
    return hashlib.sha256(otp_code.encode()).hexdigest()


def verify_otp_code(otp_code: str, otp_hash: str) -> bool:
    return secrets.compare_digest(hash_otp_code(otp_code), otp_hash)


def create_access_token(customer_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(customer_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    return int(payload["sub"])
