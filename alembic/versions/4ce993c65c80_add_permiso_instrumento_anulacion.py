"""add_permiso_instrumento_anulacion

Revision ID: 4ce993c65c80
Revises: 8c603db1909b
Create Date: 2025-06-26 11:55:15.661303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ce993c65c80'
down_revision = '8c603db1909b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO permiso "
        "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
        "('system', now(), 'anular', 'instrumento', 'Anular 4 - instrumento', 'system', now(), '7 - Estado de Cuenta', '4 - Instrumento', false)"
    )


def downgrade():
    op.execute("delete from permiso where modelo = 'instrumento' and accion = 'anular'")
