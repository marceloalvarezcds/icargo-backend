"""Add marca column to insumo table

Revision ID: 94e4aedf34b6
Revises: ad4543052b35
Create Date: 2024-11-05 05:38:25.238892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94e4aedf34b6'
down_revision = 'ad4543052b35'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('insumo', sa.Column('marca', sa.String(length=100), nullable=True))

def downgrade():
    op.drop_column('insumo', 'marca')
