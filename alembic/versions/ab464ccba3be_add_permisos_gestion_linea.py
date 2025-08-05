"""add_permisos_gestion_linea

Revision ID: ab464ccba3be
Revises: 48e2dbe45a1f
Create Date: 2025-07-16 14:49:03.891917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab464ccba3be'
down_revision = '48e2dbe45a1f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('INSERT INTO permiso '\
        ' (modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser ) values '\
        ' (\'system\', now(), \'ver\', \'gestion_de_linea\', \'Ver Gestion de linea  \', \'system\',  now(), \'5 - Orden de Carga\', \'Gestion de Linea\', false )' )


def downgrade():
    op.execute('delete from permiso where modelo = \'texto_legal\' and accion = \'ver\' ')

