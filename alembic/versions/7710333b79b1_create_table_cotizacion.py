"""create_table_cotizacion

Revision ID: 7710333b79b1
Revises: f31a4b47c493
Create Date: 2025-03-25 15:49:01.197490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7710333b79b1'
down_revision = 'f31a4b47c493'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "moneda_cotizacion",
        sa.Column("id", sa.Integer(), nullable=False),
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
        sa.Column("gestor_carga_id", sa.Integer(), nullable=True),
        sa.Column("moneda_origen_id", sa.Integer(), nullable=False),
        sa.Column("moneda_destino_id", sa.Integer(), nullable=False),
        sa.Column(
            "fecha",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "estado", sa.String(length=30), server_default="Activo", nullable=True
        ),
        sa.Column(
            "cotizacion_moneda", sa.Numeric(precision=38, scale=10), nullable=False
        ),
        sa.ForeignKeyConstraint(["moneda_origen_id"], ["moneda.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["moneda_destino_id"], ["moneda.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["gestor_carga_id"], ["gestor_carga.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("gestor_carga_id","moneda_origen_id", "moneda_destino_id", "fecha"),
    )


def downgrade():
    op.drop_table("moneda_cotizacion")

