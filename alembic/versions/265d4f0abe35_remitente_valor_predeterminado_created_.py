"""remitente valor predeterminado created_by

Revision ID: 265d4f0abe35
Revises: d65d51ec0c6e
Create Date: 2025-02-15 15:16:58.912488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '265d4f0abe35'
down_revision = 'd65d51ec0c6e'
branch_labels = None
depends_on = None


def upgrade():
    # Cambiar el valor por defecto de created_by en la tabla 'remitente'
    op.alter_column(
        'remitente',
        'created_by',
        server_default=None,  # Si quieres eliminar el valor por defecto
        existing_type=sa.String(length=255),
        nullable=True
    )


def downgrade():
    # En la reversión, restaurar el valor por defecto si es necesario
    op.alter_column(
        'remitente',
        'created_by',
        server_default="system",  # Restaurar el valor por defecto a "system"
        existing_type=sa.String(length=255),
        nullable=True
    )