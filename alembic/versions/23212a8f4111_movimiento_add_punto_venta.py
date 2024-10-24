"""movimiento_add_punto_venta

Revision ID: 23212a8f4111
Revises: 5c04f309ea5d
Create Date: 2024-10-23 10:34:31.749677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23212a8f4111'
down_revision = '5c04f309ea5d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "movimiento", sa.Column("punto_venta_id", sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column("movimiento", "punto_venta_id")
