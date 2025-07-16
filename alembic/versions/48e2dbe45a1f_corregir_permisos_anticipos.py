"""corregir_permisos_anticipos

Revision ID: 48e2dbe45a1f
Revises: 172eeeb1482c
Create Date: 2025-07-16 13:48:04.421422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48e2dbe45a1f'
down_revision = '172eeeb1482c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE permiso
        SET modulo = '5 - Orden de Carga',
            modelo_titulo = '5 - Anticipo Retirado'
        WHERE accion = 'crear_efectivo'
          AND modelo = 'orden_carga_anticipo_retirado'
    """)

    op.execute("""
        UPDATE permiso
        SET modulo = '5 - Orden de Carga',
            modelo_titulo = '5 - Anticipo Retirado'
        WHERE accion = 'crear_insumo'
          AND modelo = 'orden_carga_anticipo_retirado'
    """)


def downgrade():
    pass

