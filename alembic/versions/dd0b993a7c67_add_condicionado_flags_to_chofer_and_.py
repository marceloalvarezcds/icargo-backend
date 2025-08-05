"""Add condicionado flags to Chofer and Propietario

Revision ID: dd0b993a7c67
Revises: a58d29fd3053
Create Date: 2025-07-08 07:44:10.345494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd0b993a7c67'
down_revision = 'a58d29fd3053'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('chofer', sa.Column(
        'is_chofer_condicionado',
        sa.Boolean(),
        nullable=False,
        server_default=sa.text('false')
    ))

    op.add_column('propietario', sa.Column(
        'is_propietario_condicionado',
        sa.Boolean(),
        nullable=False,
        server_default=sa.text('false')
    ))


def downgrade():
    op.drop_column('chofer', 'is_chofer_condicionado')
    op.drop_column('propietario', 'is_propietario_condicionado')
