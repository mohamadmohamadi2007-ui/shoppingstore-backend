from sqlmodel import SQLModel, Field
from datetime import datetime, timezone



class CategoryBase(SQLModel):
    name: str
    slug: str = Field(unique=True, index=True)
    parent_id: int | None = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CategoryCreate(CategoryBase):
    pass