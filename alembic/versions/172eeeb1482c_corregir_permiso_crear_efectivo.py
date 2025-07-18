"""Corregir permiso crear_efectivo

Revision ID: 172eeeb1482c
Revises: 55eb7292c082
Create Date: 2025-07-16 13:28:07.125602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '172eeeb1482c'
down_revision = '55eb7292c082'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE permiso
        SET
            modulo = '5 - Orden de Carga',
            modelo_titulo = '5 - Anticipo Retirado'
        WHERE
            accion = 'crear_efectivo' AND
            modelo = 'orden_carga_anticipo_retirado'
    """)



def downgrade():
    pass
