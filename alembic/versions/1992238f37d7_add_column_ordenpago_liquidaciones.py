"""add_column_ordenpago_liquidaciones

Revision ID: 1992238f37d7
Revises: 43921d92138f
Create Date: 2025-04-10 16:15:47.360139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1992238f37d7'
down_revision = '43921d92138f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidacion", sa.Column("es_orden_pago", sa.BOOLEAN(), server_default=sa.text("false"))
    )


def downgrade():
    op.drop_column("liquidacion", "es_orden_pago")
