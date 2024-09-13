"""add_monto_liquidacion

Revision ID: a430f1596d0a
Revises: 836f5cae474d
Create Date: 2024-09-13 15:15:11.294968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a430f1596d0a'
down_revision = '836f5cae474d'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "liquidacion", sa.Column("pago_cobro", sa.Numeric(precision=38, scale=10), nullable=True)
    )

    op.add_column(
        "liquidacion", sa.Column("es_pago_cobro", sa.String(length=10), nullable=True)
    )


def downgrade():

    op.drop_column("liquidacion", "pago_cobro")
    op.drop_column("liquidacion", "es_pago_cobro")
