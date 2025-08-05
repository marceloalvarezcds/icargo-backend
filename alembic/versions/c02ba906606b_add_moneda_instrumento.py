"""add_moneda_instrumento

Revision ID: c02ba906606b
Revises: bbf3c885b08e
Create Date: 2025-04-07 17:14:24.632191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c02ba906606b'
down_revision = 'bbf3c885b08e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "instrumento", sa.Column("moneda_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "instrumento", sa.Column("monto_ml", sa.Numeric(precision=28, scale=10), nullable=True)
    )
    op.add_column(
        "instrumento", sa.Column("tipo_cambio_moneda", sa.Numeric(precision=28, scale=10), nullable=True)
    )
    op.create_foreign_key("fk_instrumento_moneda", "instrumento", "moneda", ["moneda_id"], ["id"])


def downgrade():
    op.drop_constraint("fk_instrumento_moneda", "instrumento", type_="foreignkey")
    op.drop_column("instrumento", "moneda_id")
    op.drop_column("instrumento", "monto_ml")
    op.drop_column("instrumento", "tipo_cambio_moneda")
