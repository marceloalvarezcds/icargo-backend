"""Add columns orden_carga

Revision ID: bbf3c885b08e
Revises: 934f81ce0d79
Create Date: 2025-04-07 12:29:13.434463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbf3c885b08e'
down_revision = '934f81ce0d79'
branch_labels = None
depends_on = None


def upgrade():
    # Para la tabla orden_carga
    op.add_column('orden_carga', sa.Column('condicion_gestor_carga_tarifa_ml', sa.Float(), nullable=True))
    op.add_column('orden_carga', sa.Column('condicion_propietario_tarifa_ml', sa.Float(), nullable=True))
    op.add_column('orden_carga', sa.Column('merma_gestor_carga_valor_ml', sa.Float(), nullable=True))
    op.add_column('orden_carga', sa.Column('merma_propietario_valor_ml', sa.Float(), nullable=True))

    # Para la tabla orden_carga_complemento
    op.add_column('orden_carga_complemento', sa.Column('remitente_monto_ml', sa.Float(), nullable=True))
    op.add_column('orden_carga_complemento', sa.Column('propietario_monto_ml', sa.Float(), nullable=True))

    # Para la tabla orden_carga_descuento
    op.add_column('orden_carga_descuento', sa.Column('proveedor_monto_ml', sa.Float(), nullable=True))
    op.add_column('orden_carga_descuento', sa.Column('propietario_monto_ml', sa.Float(), nullable=True))

def downgrade():
    # Para revertir las columnas, puedes eliminarlas nuevamente si es necesario
    op.drop_column('orden_carga', 'condicion_gestor_carga_tarifa_ml')
    op.drop_column('orden_carga', 'condicion_propietario_tarifa_ml')
    op.drop_column('orden_carga', 'merma_gestor_carga_valor_ml')
    op.drop_column('orden_carga', 'merma_propietario_valor_ml')

    op.drop_column('orden_carga_complemento', 'remitente_monto_ml')
    op.drop_column('orden_carga_complemento', 'propietario_monto_ml')

    op.drop_column('orden_carga_descuento', 'proveedor_monto_ml')
    op.drop_column('orden_carga_descuento', 'propietario_monto_ml')
