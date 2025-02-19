"""insert_tipo_mov_fiscal

Revision ID: 58e82ce16ce9
Revises: 23212a8f4111
Create Date: 2024-10-31 13:27:32.496319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58e82ce16ce9'
down_revision = '23212a8f4111'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # op.execute('insert into tipo_movimiento '\
    #     ' (created_by, created_at, modified_by, modified_at, id, descripcion, estado, cuenta_id, codigo ) '\
    #     ' values (\'system\', now(), \'system\', now(), 15, \'Fiscal\', \'Activo\', 4, \'8\' )' )


def downgrade():
    pass
    # op.execute('delete from tipo_movimiento where descripcion = \'Fiscal\' ')
