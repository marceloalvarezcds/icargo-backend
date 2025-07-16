"""add_permisos_oc

Revision ID: 55eb7292c082
Revises: 6f0b76385ff4
Create Date: 2025-07-16 13:01:49.975751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55eb7292c082'
down_revision = '6f0b76385ff4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'anticipo\', \'orden_carga\', \'Anticipo 1 - orden de carga \', \'system\',  now(), \'5 - Orden de Carga\', \'1 - Orden de Carga\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'recepcionar\', \'orden_carga\', \'Recepcionar 1 - orden de carga\', \'system\',  now(), \'5 - Orden de Carga\', \'1 - Orden de Carga\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'finalizar\', \'orden_carga\', \'Finalizar 1 - orden de carga\', \'system\',  now(), \'5 - Orden de Carga\', \'1 - Orden de Carga\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'crear_efectivo\', \'orden_carga_anticipo_retirado\', \'Crear Efectivo 5 - anticipo retirado\', \'system\',  now(), \'5 - Orden de Carga\', \'5 - Anticipo Retirado\', false )' )
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'crear_insumo\', \'orden_carga_anticipo_retirado\', \'Crear Insumo 5 - anticipo retirado\', \'system\',  now(), \'Crear Insumo 5 - anticipo retirado\', \'5 - Anticipo Retirado\', false )' )



def downgrade():
    op.execute('delete from permiso where modelo = \'orden_carga\' and accion = \'anticipo\' ')
    op.execute('delete from permiso where modelo = \'orden_carga\' and accion = \'recepcionar\' ')
    op.execute('delete from permiso where modelo = \'orden_carga\' and accion = \'finalizar\' ')
    op.execute('delete from permiso where modelo = \'orden_carga_anticipo_retirado\' and accion = \'crear_efectivo\' ')
    op.execute('delete from permiso where modelo = \'orden_carga_anticipo_retirado\' and accion = \'crear_insumo\' ')
