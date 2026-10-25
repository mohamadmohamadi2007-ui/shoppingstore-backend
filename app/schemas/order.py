from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from app.schemas.variant import Variant


class OrderBase(SQLModel):
    customer_id: int
    status: str = "pending"
    total: float = 0 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Order(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="order.id")
    variant_id: int = Field(foreign_key="variant.id")
    qty: int 
    price: float

class OrderItem(OrderItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order: Order = Relationship(back_populates="items")
    variant: Variant = Relationship()

class OrderItemRead(SQLModel):
    id: int
    variant_id: int
    qty: int
    price: float
    variant: Variant

class OrderRead(SQLModel):
    id: int
    customer_id: int
    total: float
    status: str
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemRead]