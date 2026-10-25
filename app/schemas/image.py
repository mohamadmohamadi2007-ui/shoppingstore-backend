from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class ProductImageBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    variant_id: int | None = Field(default=None, foreign_key="variant.id")
    url: str
    sort_order: int = 0
    is_primary: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



class ProductImage(ProductImageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ProductImageCreate(SQLModel):
    variant_id: int | None = None
    url: str
    sort_order: int = 0
    is_primary: bool = False