"""factura_add_column_iva

Revision ID: 5c04f309ea5d
Revises: 8d8e06da0b2c
Create Date: 2024-10-16 08:49:22.918605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c04f309ea5d'
down_revision = '8d8e06da0b2c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "factura", sa.Column("iva", sa.Numeric(precision=28, scale=10), nullable=True)
    )
    op.add_column(
        "factura", sa.Column("retencion", sa.Numeric(precision=28, scale=10), nullable=True)
    )
    op.add_column(
        "factura", sa.Column("timbrado", sa.Integer(), nullable=True)
    )
    op.add_column(
        "factura", sa.Column("contribuyente", sa.String(length=50), nullable=True)
    )
    op.add_column(
        "factura", sa.Column("ruc", sa.String(length=25), nullable=True)
    )
    op.add_column(
        "factura", sa.Column("fecha_factura", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "factura", sa.Column('iva_incl', sa.Boolean(), nullable=True, default=False)
    )
    op.add_column(
        "factura", sa.Column('es_pago', sa.Boolean(), nullable=True, default=False)
    )
    op.add_column(
        "factura", sa.Column('es_cobro', sa.Boolean(), nullable=True, default=False)
    )


def downgrade():
    op.drop_column("factura", "iva")
    op.drop_column("factura", "retencion")
    op.drop_column("factura", "timbrado")
    op.drop_column("factura", "contribuyente")
    op.drop_column("factura", "ruc")
    op.drop_column("factura", "fecha_factura")
    op.drop_column("factura", "iva_incl")
    op.drop_column("factura", "es_pago")
    op.drop_column("factura", "es_cobro")

