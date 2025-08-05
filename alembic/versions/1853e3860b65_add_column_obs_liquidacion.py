"""add_column_obs_liquidacion

Revision ID: 1853e3860b65
Revises: cb4e1cb888ce
Create Date: 2025-07-14 11:29:53.434632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1853e3860b65'
down_revision = 'cb4e1cb888ce'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "liquidacion", sa.Column("observacion", sa.String(length=255), nullable=True)
    )


def downgrade():
    op.drop_column("liquidacion", "observacion")
