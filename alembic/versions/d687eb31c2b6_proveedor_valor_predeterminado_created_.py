"""proveedor valor predeterminado created_by

Revision ID: d687eb31c2b6
Revises: 0d389d76cf15
Create Date: 2025-02-16 08:35:22.209621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd687eb31c2b6'
down_revision = '0d389d76cf15'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column(
        'proveedor',
        'created_by',
        server_default=None,  
        existing_type=sa.String(length=255),
        nullable=True
    )


def downgrade():
    op.alter_column(
        'proveedor',
        'created_by',
        server_default="system", 
        existing_type=sa.String(length=255),
        nullable=True
    )