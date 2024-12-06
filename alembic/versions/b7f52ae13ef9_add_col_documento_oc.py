"""add_col_documento_oc

Revision ID: b7f52ae13ef9
Revises: b3cbe3bf846f
Create Date: 2024-12-02 07:49:50.158081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7f52ae13ef9'
down_revision = 'b3cbe3bf846f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "orden_carga", sa.Column("documento_fisico", sa.Boolean(), server_default=sa.text("false"), nullable=True)
    )


def downgrade():
    op.drop_column("orden_carga", "documento_fisico")
