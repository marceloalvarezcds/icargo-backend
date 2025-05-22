"""add columns promedios

Revision ID: 13429062c0d1
Revises: f1ccaf3bba91
Create Date: 2025-04-30 13:25:18.841429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13429062c0d1'
down_revision = 'f1ccaf3bba91'
branch_labels = None
depends_on = None


def upgrade():
    # orden_carga_evaluaciones_historial
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_tracto_gestor', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_semi_gestor', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_chofer_gestor', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_propietario_gestor', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_carga_gestor', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_descarga_gestor', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_tracto_general', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_semi_general', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_chofer_general', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_propietario_general', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_carga_general', sa.Numeric(38, 1)))
    op.add_column('orden_carga_evaluaciones_historial', sa.Column('promedio_descarga_general', sa.Numeric(38, 1)))

    # camion
    op.add_column('camion', sa.Column('promedio_tracto_gestor', sa.Numeric(38, 1)))
    op.add_column('camion', sa.Column('promedio_tracto_general', sa.Numeric(38, 1)))
    op.add_column('camion', sa.Column('cantidad_tracto_evaluaciones', sa.Numeric(38, 1)))
    op.add_column('camion', sa.Column('cantidad_tracto_evaluaciones_gestor', sa.Numeric(38, 1)))

    # semi
    op.add_column('semi', sa.Column('promedio_semi_gestor', sa.Numeric(38, 1)))
    op.add_column('semi', sa.Column('promedio_semi_general', sa.Numeric(38, 1)))
    op.add_column('semi', sa.Column('cantidad_semi_evaluaciones', sa.Numeric(38, 1)))
    op.add_column('semi', sa.Column('cantidad_semi_evaluaciones_gestor', sa.Numeric(38, 1)))

    # chofer
    op.add_column('chofer', sa.Column('promedio_chofer_gestor', sa.Numeric(38, 1)))
    op.add_column('chofer', sa.Column('promedio_chofer_general', sa.Numeric(38, 1)))
    op.add_column('chofer', sa.Column('cantidad_chofer_evaluaciones', sa.Numeric(38, 1)))
    op.add_column('chofer', sa.Column('cantidad_chofer_evaluaciones_gestor', sa.Numeric(38, 1)))

    # propietario
    op.add_column('propietario', sa.Column('promedio_propietario_gestor', sa.Numeric(38, 1)))
    op.add_column('propietario', sa.Column('promedio_propietario_general', sa.Numeric(38, 1)))
    op.add_column('propietario', sa.Column('cantidad_propietario_evaluaciones', sa.Numeric(38, 1)))
    op.add_column('propietario', sa.Column('cantidad_propietario_evaluaciones_gestor', sa.Numeric(38, 1)))


def downgrade():
    op.drop_column('propietario', 'cantidad_propietario_evaluaciones_gestor')
    op.drop_column('propietario', 'cantidad_propietario_evaluaciones')
    op.drop_column('propietario', 'promedio_propietario_general')
    op.drop_column('propietario', 'promedio_propietario_gestor')

    op.drop_column('chofer', 'cantidad_chofer_evaluaciones_gestor')
    op.drop_column('chofer', 'cantidad_chofer_evaluaciones')
    op.drop_column('chofer', 'promedio_chofer_general')
    op.drop_column('chofer', 'promedio_chofer_gestor')

    op.drop_column('semi', 'cantidad_semi_evaluaciones_gestor')
    op.drop_column('semi', 'cantidad_semi_evaluaciones')
    op.drop_column('semi', 'promedio_semi_general')
    op.drop_column('semi', 'promedio_semi_gestor')

    op.drop_column('camion', 'cantidad_tracto_evaluaciones_gestor')
    op.drop_column('camion', 'cantidad_tracto_evaluaciones')
    op.drop_column('camion', 'promedio_tracto_general')
    op.drop_column('camion', 'promedio_tracto_gestor')

    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_descarga_general')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_carga_general')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_propietario_general')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_chofer_general')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_semi_general')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_tracto_general')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_descarga_gestor')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_carga_gestor')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_propietario_gestor')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_chofer_gestor')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_semi_gestor')
    op.drop_column('orden_carga_evaluaciones_historial', 'promedio_tracto_gestor')
