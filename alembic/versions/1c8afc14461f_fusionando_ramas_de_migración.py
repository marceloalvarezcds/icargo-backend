"""Fusionando ramas de migración

Revision ID: 1c8afc14461f
Revises: 692f88241eba, f50bbd6008ae
Create Date: 2024-12-06 06:43:25.366305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c8afc14461f'
down_revision = ('692f88241eba', 'f50bbd6008ae')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
