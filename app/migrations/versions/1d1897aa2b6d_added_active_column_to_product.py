"""Added active column to product

Revision ID: 1d1897aa2b6d
Revises: f9e0454aac60
Create Date: 2021-04-22 17:55:07.635882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d1897aa2b6d'
down_revision = 'f9e0454aac60'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('product', sa.Column('active', sa.Boolean(), nullable=True, default=1))


def downgrade():
    op.drop_column('product', 'active')
