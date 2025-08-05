"""add_column_cargado_in_flete

Revision ID: 64a8422503e6
Revises: f99a83944f1c
Create Date: 2025-05-30 10:53:10.596797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64a8422503e6'
down_revision = 'f99a83944f1c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('flete',
        sa.Column('cargado', sa.Numeric(38, 10), nullable=True)
    )


def downgrade():
    op.drop_column('flete', 'cargado')
