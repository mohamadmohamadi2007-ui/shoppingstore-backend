"""add missing foreign key on productspec.product_id

Revision ID: 77fc610172c4
Revises: 80d78bb5d247
Create Date: 2026-10-26 02:11:17.513772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77fc610172c4'
down_revision: Union[str, Sequence[str], None] = '80d78bb5d247'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        "fk_productspec_product_id_product",
        "productspec", "product", ["product_id"], ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_productspec_product_id_product", "productspec", type_="foreignkey",
    )
