"""Add permiso gestor_carga

Revision ID: e012f3391dab
Revises: d41bf937c907
Create Date: 2025-07-11 08:54:58.507614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e012f3391dab'
down_revision = 'd41bf937c907'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO permiso "
        "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'cambiar_estado', 'gestor_carga', 'Cambiar Estado Gestor de Carga', 'system', now(), '2 - Entidades', '5 - Gestor de Carga', false)"
    )


def downgrade():
    op.execute("delete from permiso where modelo = 'gestor_carga' and accion = 'cambiar_estado'")
