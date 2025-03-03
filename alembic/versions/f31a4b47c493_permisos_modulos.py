"""permisos_modulos

Revision ID: f31a4b47c493
Revises: dfbd062c3726
Create Date: 2025-03-02 09:12:56.628585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f31a4b47c493'
down_revision = 'dfbd062c3726'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(' update permiso '\
         ' set modulo = \'4 - Pedido\' '\
         ' where modulo = \'4 - Flete\' ' )



def downgrade():
    op.execute(' update permiso '\
         ' set modulo = \'4 - Flete\' '\
         ' where modulo = \'4 - Pedido\' ' )
