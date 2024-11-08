"""add column in pdv_precio

Revision ID: da60a4ecebd4
Revises: 75d556d1d1e3
Create Date: 2024-11-08 08:41:21.026965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da60a4ecebd4'
down_revision = '75d556d1d1e3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('insumo_punto_venta_precio', sa.Column('observacion', sa.String(length=255), nullable=True))
    op.add_column('insumo_punto_venta_precio', sa.Column('hora_inicio', sa.Time(), nullable=True))


def downgrade():
    op.drop_column('insumo_punto_venta_precio', 'observacion')
    op.drop_column('insumo_punto_venta_precio', 'hora_inicio')
