"""centro operativo valor predeterminado created_by

Revision ID: 64743edb7fbb
Revises: 68a4782dc23d
Create Date: 2025-02-15 15:54:50.886271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64743edb7fbb'
down_revision = '68a4782dc23d'
branch_labels = None
depends_on = None


def upgrade():
    # Cambiar el valor por defecto de created_by en la tabla 'remitente'
    op.alter_column(
        'centro_operativo',
        'created_by',
        server_default=None,  # Si quieres eliminar el valor por defecto
        existing_type=sa.String(length=255),
        nullable=True
    )


def downgrade():
    # En la reversión, restaurar el valor por defecto si es necesario
    op.alter_column(
        'centro_operativo',
        'created_by',
        server_default="system",  # Restaurar el valor por defecto a "system"
        existing_type=sa.String(length=255),
        nullable=True
    )