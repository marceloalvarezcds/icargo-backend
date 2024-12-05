"""Add ratings to orden_carga_evaluaciones_historial

Revision ID: 37f2e8a36cd6
Revises: 434ae6da6f7d
Create Date: 2024-11-29 07:39:17.248161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37f2e8a36cd6'
down_revision = '434ae6da6f7d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('tracto_rating', sa.Integer(), nullable=True))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('semi_rating', sa.Integer(), nullable=True))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('chofer_rating', sa.Integer(), nullable=True))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('propietario_rating', sa.Integer(), nullable=True))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('carga_rating', sa.Integer(), nullable=True))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('descarga_rating', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('orden_carga_evaluaciones_historial', 'descarga_rating')
    op.drop_column('orden_carga_evaluaciones_historial', 'carga_rating')
    op.drop_column('orden_carga_evaluaciones_historial', 'propietario_rating')
    op.drop_column('orden_carga_evaluaciones_historial', 'chofer_rating')
    op.drop_column('orden_carga_evaluaciones_historial', 'semi_rating')
    op.drop_column('orden_carga_evaluaciones_historial', 'tracto_rating')
