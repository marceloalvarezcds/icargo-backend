"""add_permisos_texto_legal

Revision ID: b4a79d342c59
Revises: d687eb31c2b6
Create Date: 2025-02-21 08:51:29.827317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4a79d342c59'
down_revision = 'd687eb31c2b6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'cambiar_estado\', \'texto_legal\', \'Cambiar el estado \', \'system\',  now(), \'Parámetros del Sistema\', \'Texto Legal\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'crear\', \'texto_legal\', \'Crear - Texto Legal\', \'system\',  now(), \'Parámetros del Sistema\', \'Texto Legal\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'editar\', \'texto_legal\', \'Editar - Texto Legal\', \'system\',  now(), \'Parámetros del Sistema\', \'Texto Legal\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'ver\', \'texto_legal\', \'Ver - Texto Legal\', \'system\',  now(), \'Parámetros del Sistema\', \'Texto Legal\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'listar\', \'texto_legal\', \'Ver - Texto Legal\', \'system\',  now(), \'Parámetros del Sistema\', \'Texto Legal\', false )' )



def downgrade():
    op.execute('delete from permiso where modelo = \'texto_legal\' and accion = \'cambiar_estado\' ')
    op.execute('delete from permiso where modelo = \'texto_legal\' and accion = \'crear\' ')
    op.execute('delete from permiso where modelo = \'texto_legal\' and accion = \'editar\' ')
    op.execute('delete from permiso where modelo = \'texto_legal\' and accion = \'ver\' ')
    op.execute('delete from permiso where modelo = \'texto_legal\' and accion = \'listar\' ')
