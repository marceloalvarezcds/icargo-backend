"""Change google column

Revision ID: 5650486ef409
Revises: b6023c2a44b1
Create Date: 2021-04-15 09:35:25.127775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5650486ef409'
down_revision = 'b6023c2a44b1'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'google_token')
    op.add_column('users', sa.Column('google_user', sa.Boolean(), default=False, server_default='f'))


def downgrade():
    op.drop_column('users', 'google_user')
    op.add_column('users', sa.Column('google_token', sa.String(), nullable=True))
