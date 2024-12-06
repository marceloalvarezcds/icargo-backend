"""movimiento_add_col_linea

Revision ID: f50bbd6008ae
Revises: 16b5af41e2ba
Create Date: 2024-12-05 07:47:06.449364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f50bbd6008ae'
down_revision = '16b5af41e2ba'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "movimiento", sa.Column("linea_movimiento", sa.String(length=30), nullable=True)
    )


def downgrade():
    op.drop_column("movimiento", "linea_movimiento")
