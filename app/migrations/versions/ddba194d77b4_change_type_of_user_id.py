"""Change type of user id

Revision ID: ddba194d77b4
Revises: 4ad3f83a84f0
Create Date: 2021-04-29 22:02:48.528601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddba194d77b4'
down_revision = '4ad3f83a84f0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'id', existing_type=sa.Integer, type_=sa.BigInteger)


def downgrade():
    op.alter_column('users', 'id', existing_type=sa.BigInteger, type_=sa.Integer)
