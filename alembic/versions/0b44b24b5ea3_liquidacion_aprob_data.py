"""liquidacion_aprob_data

Revision ID: 0b44b24b5ea3
Revises: a430f1596d0a
Create Date: 2024-09-17 08:47:27.272636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b44b24b5ea3'
down_revision = 'a430f1596d0a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidacion", sa.Column("user_aprueba", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "liquidacion", sa.Column("aprobado_at", sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_column("liquidacion", "user_aprueba")
    op.drop_column("liquidacion", "aprobado_at")
