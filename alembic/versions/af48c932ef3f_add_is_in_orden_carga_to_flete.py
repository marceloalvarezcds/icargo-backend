"""add_is_in_orden_carga to flete

Revision ID: af48c932ef3f
Revises: 76e4fda915a4
Create Date: 2025-05-02 10:45:04.607830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af48c932ef3f'
down_revision = '76e4fda915a4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('flete', sa.Column('is_in_orden_carga', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('flete', 'is_in_orden_carga')
