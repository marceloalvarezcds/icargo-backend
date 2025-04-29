"""alter_liquidacion_tipo_mov

Revision ID: bf9daf409e22
Revises: 1992238f37d7
Create Date: 2025-04-24 09:27:44.647830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf9daf409e22'
down_revision = '1992238f37d7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'liquidacion',
        'tipo_mov_liquidacion',
        existing_type=sa.String(length=10),
        type_=sa.String(length=20)
    )


def downgrade():
    op.alter_column(
        'liquidacion',
        'tipo_mov_liquidacion',
        existing_type=sa.String(length=20),
        type_=sa.String(length=10),
    )
