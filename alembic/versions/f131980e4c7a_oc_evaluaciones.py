"""oc_evaluaciones

Revision ID: f131980e4c7a
Revises: 52327a99d747
Create Date: 2024-09-25 08:58:33.437584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f131980e4c7a'
down_revision = '52327a99d747'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    "orden_carga_evaluaciones_historial",
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("orden_carga_id", sa.Integer(), nullable=True),
    sa.Column("comentario", sa.String(length=255), nullable=True),
    sa.Column("created_by", sa.String(length=100), nullable=True),
    sa.Column("modified_by", sa.String(length=100), nullable=True),
    sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
    sa.Column("modified_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
    sa.Column("tipo_incidente_id", sa.Integer(), nullable=True),
    sa.Column("comentarios", sa.String(length=255), nullable=True),
    sa.Column("gestor_carga_id", sa.Integer(), nullable=True),
    sa.Column("camion_id", sa.Integer(), nullable=True),
    sa.Column("semi_id", sa.Integer(), nullable=True),
    sa.Column("propietario_id", sa.Integer(), nullable=True),
    sa.Column("chofer_id", sa.Integer(), nullable=True),
    sa.Column("concepto", sa.String(length=255), nullable=True),
    sa.Column("nota", sa.String(length=255), nullable=True),
    sa.Column("origen_id", sa.Integer(), nullable=True),
    sa.Column("destino_id", sa.Integer(), nullable=True),
    sa.Column("producto_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(
        ["orden_carga_id"],
        ["orden_carga.id"],
        ondelete="SET NULL"
    ),
    sa.ForeignKeyConstraint(
        ["tipo_incidente_id"],
        ["tipo_incidente.id"],
        ondelete="SET NULL"
    )
    )


def downgrade():
    op.drop_constraint('fk_orden_carga', 'orden_carga_evaluaciones_historial', type_='foreignkey')
    op.drop_constraint('fk_tipo_incidente', 'orden_carga_evaluaciones_historial', type_='foreignkey')
    op.drop_table("orden_carga_evaluaciones_historial")
