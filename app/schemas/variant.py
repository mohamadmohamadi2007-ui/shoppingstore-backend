from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class VariantBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    sku: str = Field(unique=True, index=True)
    band: str | None = None
    cup: str | None = None
    size_label: str | None = None
    color: str
    price_override: float | None = None
    stock_qty: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



class Variant(VariantBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class VariantCreate(VariantBase):
    pass

class VariantUpdate(SQLModel):
    color: str
    price_override: float | None = None
    stock_qty: int