"""remove address from user

Revision ID: 7d0fea047c4f
Revises: ddba194d77b4
Create Date: 2021-04-29 22:18:16.487098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d0fea047c4f'
down_revision = 'ddba194d77b4'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'address')


def downgrade():
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))
