"""add_constrain_uk_pdv

Revision ID: 1b5a6ddd22e4
Revises: 87f081d371dd
Create Date: 2025-07-22 14:48:37.690005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b5a6ddd22e4'
down_revision = '87f081d371dd'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "punto_venta_tipo_documento_id_numero_documento_key",
        "punto_venta",
        type_="unique",
    )
    op.create_unique_constraint(
        "punto_venta_tipo_documento_id_numero_documento_key",
        "punto_venta",
        [
            "tipo_documento_id",
            "numero_documento",
            "numero_sucursal"
        ],
    )


def downgrade():
    op.drop_constraint(
        "punto_venta_tipo_documento_id_numero_documento_key",
        "punto_venta",
        type_="unique",
    )
