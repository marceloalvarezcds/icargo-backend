"""add_permisos_evaluacion

Revision ID: 42ce6b07aff6
Revises: 13429062c0d1
Create Date: 2025-05-02 08:13:45.317430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42ce6b07aff6'
down_revision = '13429062c0d1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO permiso "
        "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'listar', 'orden_carga_evaluacion', 'Listar 10 - evaluacion', 'system', now(), '5 - Orden de Carga', 'Evaluacion', false)"
    )
    ##op.execute(
    ##    "INSERT INTO permiso "
    ##    "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
    ##    "('system', now(), 'crear', 'orden_carga_evaluacion', 'Crear 10 - evaluacion', 'system', now(), '5 - Orden de Carga', 'Evaluacion', false)"
    ##)
    ##op.execute(
    ##    "INSERT INTO permiso "
    ##    "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
    ##    "('system', now(), 'ver', 'orden_carga_evaluacion', 'Ver 10 - evaluacion', 'system', now(), '5 - Orden de Carga', 'Evaluacion', false)"
    ##)

def downgrade():
    op.execute("delete from permiso where modelo = 'orden_carga_evaluacion' and accion = 'listar'")
    op.execute("delete from permiso where modelo = 'orden_carga_evaluacion' and accion = 'crear'")
    op.execute("delete from permiso where modelo = 'orden_carga_evaluacion' and accion = 'ver'")
