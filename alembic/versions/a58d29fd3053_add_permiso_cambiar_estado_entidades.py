"""add_permiso_cambiar_estado_entidades

Revision ID: a58d29fd3053
Revises: 4ce993c65c80
Create Date: 2025-06-26 12:14:27.790303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a58d29fd3053'
down_revision = '4ce993c65c80'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'cambiar_estado\', \'remitente\', \'Cambiar de Estado 2 - remitente \', \'system\',  now(), \'2 - Entidades\', \'2 - Remitente\', false )' )

    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'cambiar_estado\', \'centro_operativo\', \'Cambiar de Estado - Centro Operativo \', \'system\',  now(), \'2 - Entidades\', \'1 - Centro Operativo\', false )' )

    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'cambiar_estado\', \'proveedor\', \'Cambiar de Estado 3 - proveedor\', \'system\',  now(), \'2 - Entidades\', \'3 - Proveedor\', false )' )


def downgrade():
    op.execute('delete from permiso where modelo = \'remitente\' and accion = \'cambiar_estado\' ')
    op.execute('delete from permiso where modelo = \'centro_operativo\' and accion = \'cambiar_estado\' ')
    op.execute('delete from permiso where modelo = \'proveedor\' and accion = \'cambiar_estado\' ')
