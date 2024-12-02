"""add_pdv_columns

Revision ID: 27139fe9088e
Revises: 5c04f309ea5d
Create Date: 2024-10-31 09:01:10.254590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27139fe9088e'
down_revision = '5c04f309ea5d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "provision",
        sa.Column(
            "created_by", sa.String(length=255), server_default="system", nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "modified_by", sa.String(length=255), server_default="system", nullable=True
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("gestor_carga_id", sa.Integer(), nullable=True),
        sa.Column("liquidacion_id", sa.Integer(), nullable=True),
        sa.Column("orden_carga_id", sa.Integer(), nullable=True),
        sa.Column(
            "estado", sa.String(length=255), server_default="Pendiente", nullable=True
        ),
        sa.Column("tipo_contraparte_id", sa.Integer(), nullable=True),
        sa.Column("contraparte", sa.String(length=255), nullable=True),
        sa.Column("contraparte_numero_documento", sa.String(length=255), nullable=True),
        sa.Column("tipo_documento_relacionado_id", sa.Integer(), nullable=True),
        sa.Column("numero_documento_relacionado", sa.String(length=255), nullable=True),
        sa.Column("cuenta_id", sa.Integer(), nullable=True),
        sa.Column("tipo_movimiento_id", sa.Integer(), nullable=True),
        sa.Column("monto", sa.Numeric(precision=38, scale=10), nullable=True),
        sa.Column("moneda_id", sa.Integer(), nullable=True),
        sa.Column(
            "tipo_cambio_moneda", sa.Numeric(precision=38, scale=10), nullable=True
        ),
        sa.Column("fecha_cambio_moneda", sa.DateTime(), nullable=True),
        sa.Column("anticipo_id", sa.Integer(), nullable=True),
        sa.Column("complemento_id", sa.Integer(), nullable=True),
        sa.Column("descuento_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["anticipo_id"],
            ["orden_carga_anticipo_retirado.id"],
        ),
        sa.ForeignKeyConstraint(
            ["complemento_id"],
            ["orden_carga_complemento.id"],
        ),
        sa.ForeignKeyConstraint(
            ["cuenta_id"],
            ["tipo_cuenta.id"],
        ),
        sa.ForeignKeyConstraint(
            ["descuento_id"],
            ["orden_carga_descuento.id"],
        ),
        sa.ForeignKeyConstraint(
            ["gestor_carga_id"],
            ["gestor_carga.id"],
        ),
        sa.ForeignKeyConstraint(
            ["liquidacion_id"],
            ["liquidacion.id"],
        ),
        sa.ForeignKeyConstraint(
            ["moneda_id"],
            ["moneda.id"],
        ),
        sa.ForeignKeyConstraint(
            ["orden_carga_id"],
            ["orden_carga.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tipo_contraparte_id"],
            ["tipo_contraparte.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tipo_documento_relacionado_id"],
            ["tipo_documento_relacionado.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tipo_movimiento_id"],
            ["tipo_movimiento.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("provision")
