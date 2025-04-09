"""add saldos columns

Revision ID: 5b93163d270a
Revises: c02ba906606b
Create Date: 2025-04-09 06:49:19.902023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b93163d270a'
down_revision = 'c02ba906606b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orden_carga_anticipo_saldo', sa.Column('saldo_ml', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('orden_carga_anticipo_saldo', sa.Column('total_anticipo_ml', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('orden_carga_anticipo_saldo', sa.Column('total_retirado_ml', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('orden_carga_anticipo_retirado', sa.Column('monto_mon_local', sa.Numeric(precision=10, scale=2), nullable=True))


def downgrade():
    op.drop_column('orden_carga_anticipo_saldo', 'saldo_ml')
    op.drop_column('orden_carga_anticipo_saldo', 'total_anticipo_ml')
    op.drop_column('orden_carga_anticipo_saldo', 'total_retirado_ml')
    op.drop_column('orden_carga_anticipo_retirado', 'monto_mon_local')
