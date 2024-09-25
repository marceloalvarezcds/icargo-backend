"""oc_comentarios_historial

Revision ID: 452cf76ae03b
Revises: d2ad97f8c443
Create Date: 2024-09-25 07:43:36.207639

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '452cf76ae03b'
down_revision = 'd2ad97f8c443'
branch_labels = None
depends_on = None


def upgrade():
        # Create the orden_carga_comentarios_historial table
    op.create_table(
        "orden_carga_comentarios_historial",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("orden_carga_id", sa.Integer(), nullable=True),
        sa.Column("comentario", sa.String(), nullable=True),
        sa.Column("created_by", sa.String(length=255), server_default="system", nullable=True),
        sa.Column("modified_by", sa.String(length=255), server_default="system", nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.Column("modified_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.ForeignKeyConstraint(
            ["orden_carga_id"],
            ["orden_carga.id"],
            ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("orden_carga_comentarios_historial")
