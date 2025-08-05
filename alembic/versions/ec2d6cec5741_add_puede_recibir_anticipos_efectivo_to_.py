"""add puede_recibir_anticipos_efectivo to punto_venta

Revision ID: ec2d6cec5741
Revises: 64a8422503e6
Create Date: 2025-06-11 15:30:38.188385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec2d6cec5741'
down_revision = '64a8422503e6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('punto_venta',
        sa.Column('puede_recibir_anticipos_efectivo', sa.Boolean(), server_default=sa.text('true'), nullable=False)
    )


def downgrade():
    op.drop_column('punto_venta', 'puede_recibir_anticipos_efectivo')
