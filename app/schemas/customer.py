from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class CustomerBase(SQLModel):
    phone_number: str = Field(unique=True, index=True)
    full_name: str | None = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    otp_code_hash: str | None = Field(default=None)
    otp_expires_at: datetime | None = Field(default=None)


class CustomerRead(SQLModel):
    id: int
    phone_number: str
    full_name: str | None
    is_active: bool
    created_at: datetime
