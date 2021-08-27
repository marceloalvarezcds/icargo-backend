"""Add token columns to user

Revision ID: b6023c2a44b1
Revises: 
Create Date: 2021-04-12 10:34:33.970508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6023c2a44b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('fb_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('google_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('apple_token', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'token')
    op.drop_column('users', 'fb_token')
    op.drop_column('users', 'google_token')
    op.drop_column('users', 'apple_token')
