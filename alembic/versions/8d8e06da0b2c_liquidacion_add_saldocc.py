"""liquidacion_add_saldocc

Revision ID: 8d8e06da0b2c
Revises: daee2af2a460
Create Date: 2024-10-13 08:43:21.335360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d8e06da0b2c'
down_revision = 'daee2af2a460'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidacion", sa.Column("saldo_cc", sa.Numeric(precision=38, scale=10), nullable=True)
    )


def downgrade():
    op.drop_column("liquidacion", "saldo_cc")
