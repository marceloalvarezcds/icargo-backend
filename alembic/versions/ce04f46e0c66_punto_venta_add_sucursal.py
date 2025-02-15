"""punto_venta_add_sucursal

Revision ID: ce04f46e0c66
Revises: 7c0fba344d05
Create Date: 2025-02-14 15:18:59.495865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce04f46e0c66'
down_revision = '7c0fba344d05'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "punto_venta", sa.Column("numero_sucursal", sa.Integer(), nullable=True)
    )
    op.create_unique_constraint(
        "punto_venta_proveedor_sucursal_uk",
        "punto_venta",
        [
            "proveedor_id",
            "numero_sucursal",
        ],
    )


def downgrade():
    op.drop_column("punto_venta", "numero_sucursal")
    op.drop_constraint("punto_venta_proveedor_sucursal_uk", "punto_venta", type_="unique")
