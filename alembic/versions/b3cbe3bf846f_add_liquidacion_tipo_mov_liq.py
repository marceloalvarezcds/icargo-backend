"""add_liquidacion_tipo_mov_liq

Revision ID: b3cbe3bf846f
Revises: da60a4ecebd4
Create Date: 2024-11-22 13:59:47.895186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3cbe3bf846f'
down_revision = 'da60a4ecebd4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidacion", sa.Column("tipo_mov_liquidacion", sa.String(length=10), server_default="Efectivo", nullable=True)
    )


def downgrade():
    op.drop_column("liquidacion", "tipo_mov_liquidacion")
