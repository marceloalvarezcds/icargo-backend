"""create_constrain_factura

Revision ID: f1ccaf3bba91
Revises: bf9daf409e22
Create Date: 2025-04-28 10:19:04.733784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1ccaf3bba91'
down_revision = 'bf9daf409e22'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("factura_liquidacion_id_numero_factura_moneda_id_iva_id_key", "factura", type_="unique",)


def downgrade():
    op.create_unique_constraint(
        "factura_liquidacion_id_numero_factura_moneda_id_iva_id_key",
        "factura",
        [
            "liquidacion_id", "numero_factura", "moneda_id", "iva_id"
        ],
    )

