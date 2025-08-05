"""add anular permission for orden_carga_anticipo_retirado

Revision ID: 9d13debe4316
Revises: af48c932ef3f
Create Date: 2025-05-05 10:25:30.175781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d13debe4316'
down_revision = 'af48c932ef3f'
branch_labels = None
depends_on = None


def upgrade():
    pass
    #op.execute(
    #    "INSERT INTO permiso "
    #    "(modified_by, modified_at, accion, modelo, descripcion, created_by, created_at, modulo, modelo_titulo, is_for_superuser) VALUES "
    #    "('system', now(), 'anular', 'orden_carga_anticipo_retirado', 'Anular 5 - anticipo retirado', 'system', now(), '5 - Orden de Carga', '5 - Anticipo Retirado', false)"
    #)

def downgrade():
    op.execute("DELETE FROM permiso WHERE modelo = 'orden_carga_anticipo_retirado' AND accion = 'anular'")

