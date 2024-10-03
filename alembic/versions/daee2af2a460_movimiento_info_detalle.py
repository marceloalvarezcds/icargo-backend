"""movimiento_info_detalle

Revision ID: daee2af2a460
Revises: f131980e4c7a
Create Date: 2024-10-02 21:34:22.299205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daee2af2a460'
down_revision = 'f131980e4c7a'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column(
        "movimiento", sa.Column("tipo_movimiento_info", sa.String(length=100), nullable=True)
    )


def downgrade():
    op.drop_column("movimiento", "tipo_movimiento_info")
