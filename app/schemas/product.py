from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    product_code: str = Field(unique=True, index=True)
    name: str
    category_id: int = Field(foreign_key="category.id")
    base_price: float
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass

class ProductUpdate(SQLModel):
    name: str
    base_price: float


class ProductSpecBase(SQLModel):
    product_id: int = Field(foreign_key="product.id", unique=True)
    fabric: str
    care_instructions: str
    origin_country: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductSpec(ProductSpecBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ProductSpecCreate(ProductSpecBase):
    pass