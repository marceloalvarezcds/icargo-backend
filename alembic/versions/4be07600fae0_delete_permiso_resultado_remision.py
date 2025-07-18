"""delete_permiso_resultado_remision

Revision ID: 4be07600fae0
Revises: ab464ccba3be
Create Date: 2025-07-17 11:12:09.029519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4be07600fae0'
down_revision = 'ab464ccba3be'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        DELETE FROM permiso
        WHERE modelo = 'orden_carga_remision_resultado'
          AND accion IN ('listar', 'ver')
    """)


def downgrade():
    pass
