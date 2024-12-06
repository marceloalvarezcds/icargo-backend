"""add columns to orden_carga

Revision ID: d660ba3f6768
Revises: 37f2e8a36cd6
Create Date: 2024-12-04 10:21:00.360601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd660ba3f6768'
down_revision = '37f2e8a36cd6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orden_carga', sa.Column('chofer_id', sa.Integer(), nullable=True))
    op.add_column('orden_carga', sa.Column('propietario_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('orden_carga', 'chofer_id')
    op.drop_column('orden_carga', 'propietario_id')
