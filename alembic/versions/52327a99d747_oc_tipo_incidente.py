"""oc_tipo_incidente

Revision ID: 52327a99d747
Revises: 452cf76ae03b
Create Date: 2024-09-25 08:43:00.975849

"""
from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52327a99d747'
down_revision = '452cf76ae03b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    "tipo_incidente",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("created_by", sa.String(length=255), server_default="system", nullable=True),
    sa.Column("modified_by", sa.String(length=255), server_default="system", nullable=True),
    sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
    sa.Column("modified_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
    sa.Column("descripcion", sa.String(), nullable=True),
    sa.Column("estado", sa.String(), nullable=True),
    sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("tipo_incidente")
