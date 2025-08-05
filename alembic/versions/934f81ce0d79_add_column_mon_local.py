"""add_column_mon_local

Revision ID: 934f81ce0d79
Revises: 7710333b79b1
Create Date: 2025-03-31 13:30:24.959784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '934f81ce0d79'
down_revision = '7710333b79b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "movimiento", sa.Column("monto_mon_local", sa.Numeric(precision=38, scale=10), nullable=True)
    )


def downgrade():
    op.drop_column("movimiento", "monto_mon_local")
