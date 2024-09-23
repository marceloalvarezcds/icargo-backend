"""liquidacion_add_punto_venta_id

Revision ID: 59c07cc016f2
Revises: 0b44b24b5ea3
Create Date: 2024-09-18 11:56:06.325059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59c07cc016f2'
down_revision = '0b44b24b5ea3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidacion", sa.Column("punto_venta_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "fk_liquidacion_punto_venta", "liquidacion", "punto_venta", ["punto_venta_id"], ["id"]
    )


def downgrade():
    op.drop_constraint("fk_liquidacion_punto_venta", "liquidacion", type_="foreignkey")
    op.drop_column("liquidacion", "punto_venta_id")
