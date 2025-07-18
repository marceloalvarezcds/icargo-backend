"""Add is_edit column to flete

Revision ID: 24407cb885fb
Revises: b01555797f2e
Create Date: 2025-07-10 10:52:08.277933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24407cb885fb'
down_revision = 'b01555797f2e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('flete', sa.Column('is_edit', sa.Boolean(), nullable=False, server_default=sa.text('false')))


def downgrade():
    op.drop_column('flete', 'is_edit')
