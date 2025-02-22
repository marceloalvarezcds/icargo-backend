"""add_tabla_texto_legal

Revision ID: d9cea90e7162
Revises: b4a79d342c59
Create Date: 2025-02-21 10:12:32.421946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9cea90e7162'
down_revision = 'b4a79d342c59'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "texto_legal",
        sa.Column(
            "created_by", sa.String(length=255), server_default=None, nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "modified_by", sa.String(length=255), server_default=None, nullable=True
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("gestor_carga_id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=50), nullable=True),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column(
            "estado", sa.String(length=255), server_default="Activo", nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("titulo"),
    )


def downgrade():
    op.drop_table("texto_legal")
