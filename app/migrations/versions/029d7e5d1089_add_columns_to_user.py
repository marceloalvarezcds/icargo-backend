"""Add columns to user

Revision ID: 029d7e5d1089
Revises: 5650486ef409
Create Date: 2021-04-22 22:20:41.227703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '029d7e5d1089'
down_revision = '5650486ef409'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('ruc', sa.String(), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))
    op.drop_column('users', 'fb_token')
    op.drop_column('users', 'apple_token')
    op.add_column('users', sa.Column('icargo_user', sa.Boolean(), default=False, server_default='f'))
    op.add_column('users', sa.Column('fb_user', sa.Boolean(), default=False, server_default='f'))
    op.add_column('users', sa.Column('apple_user', sa.Boolean(), default=False, server_default='f'))


def downgrade():
    op.drop_column('users', 'name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'ruc')
    op.drop_column('users', 'address')
    op.drop_column('users', 'fb_user')
    op.drop_column('users', 'apple_user')
    op.drop_column('users', 'icargo_user')
    op.add_column('users', sa.Column('fb_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('apple_token', sa.String(), nullable=True))

