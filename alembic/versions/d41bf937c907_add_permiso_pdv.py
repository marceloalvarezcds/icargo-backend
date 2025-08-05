"""Add permiso pdv

Revision ID: d41bf937c907
Revises: 24407cb885fb
Create Date: 2025-07-10 16:25:05.238359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd41bf937c907'
down_revision = '24407cb885fb'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO permiso "
        "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'cambiar_estado', 'punto_venta', 'Cambiar Estado', 'system', now(), '2 - Entidades', '4 - Punto de Venta', false)"
    )


def downgrade():
    op.execute("delete from permiso where modelo = 'punto_venta' and accion = 'cambiar_estado'")
