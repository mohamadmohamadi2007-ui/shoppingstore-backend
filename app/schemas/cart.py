from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone


class CartBase(SQLModel):
    customer_id: int = Field(foreign_key="customer.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Cart(CartBase, table= True):
    id: int | None = Field(default=None, primary_key=True)
    items: list["CartItem"] = Relationship(back_populates="cart")

class CartCreate(SQLModel):
    customer_id: int


class CartItemBase(SQLModel):
    cart_id: int = Field(foreign_key="cart.id")
    variant_id: int = Field(foreign_key="variant.id")
    qty: int = 1

class CartItem(CartItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cart: Cart = Relationship(back_populates="items")

class CartItemCreate(SQLModel):
    variant_id: int
    qty: int = 1

class CartItemUpdate(SQLModel):
    qty: int

class CartItemRead(SQLModel):
    id: int
    variant_id: int
    qty: int

class CartRead(SQLModel):
    id: int
    customer_id: int
    created_at: datetime
    items: list[CartItemRead] = []

