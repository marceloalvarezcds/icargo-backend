"""permiso_cuenta_concepto_insert

Revision ID: d65d51ec0c6e
Revises: ce04f46e0c66
Create Date: 2025-02-14 15:46:03.470119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd65d51ec0c6e'
down_revision = 'ce04f46e0c66'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'cambiar_estado\', \'tipo_cuenta\', \'Cambiar el estado de Tipo Cuenta\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo de Cuenta\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'crear\', \'tipo_cuenta\', \'Crear - Tipo Cuenta\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo de Cuenta\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'editar\', \'tipo_cuenta\', \'Editar - Tipo Cuenta\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo de Cuenta\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'ver\', \'tipo_cuenta\', \'Ver - Tipo Cuenta\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo de Cuenta\', false )' )

    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'cambiar_estado\', \'tipo_movimiento\', \'Cambiar el estado de Tipo Movimiento\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo Movimiento\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'crear\', \'tipo_movimiento\', \'Crear - Tipo Movimiento\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo Movimiento\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'editar\', \'tipo_movimiento\', \'Editar - Tipo Movimiento\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo Movimiento\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'ver\', \'tipo_movimiento\', \'Ver - Tipo Movimiento\', \'system\',  now(), \'Parámetros del Sistema\', \'Tipo Movimiento\', false )' )

def downgrade():
    op.execute('delete from permiso where modelo = \'tipo_cuenta\' and accion = \'cambiar_estado\' ')
    op.execute('delete from permiso where modelo = \'tipo_cuenta\' and accion = \'crear\' ')
    op.execute('delete from permiso where modelo = \'tipo_cuenta\' and accion = \'editar\' ')
    op.execute('delete from permiso where modelo = \'tipo_cuenta\' and accion = \'ver\' ')
    op.execute('delete from permiso where modelo = \'tipo_movimiento\' and accion = \'cambiar_estado\' ')
    op.execute('delete from permiso where modelo = \'tipo_movimiento\' and accion = \'crear\' ')
    op.execute('delete from permiso where modelo = \'tipo_movimiento\' and accion = \'editar\' ')
    op.execute('delete from permiso where modelo = \'tipo_movimiento\' and accion = \'ver\' ')



