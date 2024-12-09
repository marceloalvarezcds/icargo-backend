"""hora_inicio

Revision ID: 434ae6da6f7d
Revises: b3cbe3bf846f
Create Date: 2024-11-27 13:20:57.867277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '434ae6da6f7d'
down_revision = 'b3cbe3bf846f'
branch_labels = None
depends_on = None

# se comenta debido a que migracion se duplica en revision da60a4ecebd4
def upgrade():
    pass
    #op.add_column('insumo_punto_venta_precio', sa.Column('hora_inicio', sa.String(length=8), nullable=True))


def downgrade():
    pass
    #op.drop_column('insumo_punto_venta_precio', 'hora_inicio')
