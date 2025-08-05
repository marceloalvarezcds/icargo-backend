"""add_permisos_cotizacion

Revision ID: 76e4fda915a4
Revises: 42ce6b07aff6
Create Date: 2025-05-02 10:02:44.573700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76e4fda915a4'
down_revision = '42ce6b07aff6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO permiso (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'listar', 'moneda_cotizacion', 'Listar Cotizacion', 'system', now(), '9 - Biblioteca de Usuario', 'Cotizacion', false)"
    )
    op.execute(
        "INSERT INTO permiso (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'crear', 'moneda_cotizacion', 'Crear Cotizacion', 'system', now(), '9 - Biblioteca de Usuario', 'Cotizacion', false)"
    )
    op.execute(
        "INSERT INTO permiso (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'ver', 'moneda_cotizacion', 'Ver Cotizacion', 'system', now(), '9 - Biblioteca de Usuario', 'Cotizacion', false)"
    )

def downgrade():
    op.execute("delete from permiso where modelo = 'moneda_cotizacion' and accion = 'listar'")
    op.execute("delete from permiso where modelo = 'moneda_cotizacion' and accion = 'crear'")
    op.execute("delete from permiso where modelo = 'moneda_cotizacion' and accion = 'ver'")
