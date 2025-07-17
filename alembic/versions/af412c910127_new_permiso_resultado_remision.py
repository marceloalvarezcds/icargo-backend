"""new_permiso_resultado_remision

Revision ID: af412c910127
Revises: 4be07600fae0
Create Date: 2025-07-17 11:35:01.135813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af412c910127'
down_revision = '4be07600fae0'
branch_labels = None
depends_on = None


def upgrade():
    # Actualizar el permiso "ver" gestor
    op.execute(
        "UPDATE permiso "
        "SET descripcion = 'Ver 8 - resultado de remisión de la gestora', "
        "modelo_titulo = '8 - Resultado de Remisión de la Gestora' "
        "WHERE modelo = 'orden_carga_remision_resultado_gestor' "
        "AND accion = 'ver' "
        "AND modulo = '5 - Orden de Carga'"
    )

    # Insertar permiso "listar" gestor
    op.execute(
        "INSERT INTO permiso "
        "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'listar', 'orden_carga_remision_resultado_gestor', 'Listar 8 - resultado de remisión de la gestora', 'system', now(), '5 - Orden de Carga', '8 - Resultado de Remisión de la Gestora', false)"
    )

    # Insertar permiso "listar" propietario
    op.execute(
        "INSERT INTO permiso "
        "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'listar', 'orden_carga_remision_resultado_propietario', 'Listar 9 - resultado de remisión del propietario', 'system', now(), '5 - Orden de Carga', '9 - Resultado de Remisión del Propietario', false)"
    )

    # Insertar permiso "ver" propietario
    op.execute(
        "INSERT INTO permiso "
        "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'ver', 'orden_carga_remision_resultado_propietario', 'Ver 9 - resultado de remisión del propietario', 'system', now(), '5 - Orden de Carga', '9 - Resultado de Remisión del Propietario', false)"
    )


def downgrade():
    op.execute(
        "UPDATE permiso "
        "SET descripcion = 'Ver 9 - resultado de remisión de la gestora', "
        "modelo_titulo = '9 - Resultado de Remisión de la Gestora' "
        "WHERE modelo = 'orden_carga_remision_resultado_gestor' "
        "AND accion = 'ver' "
        "AND modulo = '5 - Orden de Carga'"
    )

    op.execute("delete from permiso where modelo = 'orden_carga_remision_resultado_gestor' and accion = 'listar' and modulo = '5 - Orden de Carga'")
    op.execute("delete from permiso where modelo = 'orden_carga_remision_resultado_propietario' and accion = 'listar' and modulo = '5 - Orden de Carga'")
    op.execute("delete from permiso where modelo = 'orden_carga_remision_resultado_propietario' and accion = 'ver' and modulo = '5 - Orden de Carga'")

