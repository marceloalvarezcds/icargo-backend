"""Add hora_inicio column with String type

Revision ID: ad4543052b35
Revises: a107c1327bf6
Create Date: 2024-11-05 05:35:13.030321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad4543052b35'
down_revision = 'a107c1327bf6'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # # Agregar las columnas 'hora_inicio' y 'observacion' a la tabla 'insumo_punto_venta_precio'
    # op.add_column('insumo_punto_venta_precio', sa.Column('hora_inicio', sa.String(length=5), nullable=True))
    # op.add_column('insumo_punto_venta_precio', sa.Column('observacion', sa.String(length=255), nullable=True))

def downgrade():
    pass
    # Eliminar las columnas 'hora_inicio' y 'observacion' en caso de rollback
    # op.drop_column('insumo_punto_venta_precio', 'hora_inicio')
    # op.drop_column('insumo_punto_venta_precio', 'observacion')