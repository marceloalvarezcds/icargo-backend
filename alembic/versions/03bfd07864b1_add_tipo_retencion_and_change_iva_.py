"""add tipo_retencion and change iva_incluido to string

Revision ID: 03bfd07864b1
Revises: 1b5a6ddd22e4
Create Date: 2025-08-04 10:56:35.749312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03bfd07864b1'
down_revision = '1b5a6ddd22e4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('factura', sa.Column('tipo_retencion', sa.String(length=255), nullable=True))

    op.alter_column(
        'factura',
        'iva_incluido',
        existing_type=sa.Boolean(),
        type_=sa.String(length=255),
        postgresql_using="iva_incluido::text"
    )


def downgrade():
    op.drop_column('factura', 'tipo_retencion')

    op.alter_column(
        'factura',
        'iva_incluido',
        existing_type=sa.String(length=255),
        type_=sa.Boolean(),
        postgresql_using="iva_incluido::boolean"
    )
