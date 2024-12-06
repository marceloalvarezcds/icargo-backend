"""Add is_in_combinacion column to camion

Revision ID: 692f88241eba
Revises: d660ba3f6768
Create Date: 2024-12-05 11:01:07.843614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '692f88241eba'
down_revision = 'd660ba3f6768'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('camion', sa.Column('is_in_combinacion', sa.Boolean, nullable=False, server_default=sa.text('false')))


def downgrade():
    op.drop_column('camion', 'is_in_combinacion')
