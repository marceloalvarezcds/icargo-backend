"""add columns to flete_complemento and flete_descuento

Revision ID: 43921d92138f
Revises: 5b93163d270a
Create Date: 2025-04-10 15:49:23.986567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43921d92138f'
down_revision = '5b93163d270a'
branch_labels = None
depends_on = None


def upgrade():
    # Tabla flete_complemento
    op.add_column('flete_complemento', sa.Column('remitente_monto_ml', sa.Numeric(38, 10), nullable=True))
    op.add_column('flete_complemento', sa.Column('propietario_monto_ml', sa.Numeric(38, 10), nullable=True))

    # Tabla flete_descuento
    op.add_column('flete_descuento', sa.Column('propietario_monto_ml', sa.Numeric(38, 10), nullable=True))
    op.add_column('flete_descuento', sa.Column('proveedor_monto_ml', sa.Numeric(38, 10), nullable=True))

def downgrade():
    # Revertir cambios
    op.drop_column('flete_complemento', 'remitente_monto_ml')
    op.drop_column('flete_complemento', 'propietario_monto_ml')
    op.drop_column('flete_descuento', 'propietario_monto_ml')
    op.drop_column('flete_descuento', 'proveedor_monto_ml')
