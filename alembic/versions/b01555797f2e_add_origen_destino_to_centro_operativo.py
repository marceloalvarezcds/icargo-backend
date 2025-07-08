"""add origen_destino to centro_operativo

Revision ID: b01555797f2e
Revises: dd0b993a7c67
Create Date: 2025-07-08 16:23:58.335129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b01555797f2e'
down_revision = 'dd0b993a7c67'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('centro_operativo', sa.Column('origen_destino', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('centro_operativo', 'origen_destino')
