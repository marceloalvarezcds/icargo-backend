"""add_fecha_insumo

Revision ID: a107c1327bf6
Revises: 27139fe9088e
Create Date: 2024-11-04 09:09:58.412293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a107c1327bf6'
down_revision = '27139fe9088e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('insumo', sa.Column('fecha_creacion', sa.DateTime, nullable=True))


def downgrade():
    op.drop_column('insumo', 'fecha_creacion')

