"""pdv valor predeterminado created_by

Revision ID: 0d389d76cf15
Revises: 64743edb7fbb
Create Date: 2025-02-16 08:29:56.870803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d389d76cf15'
down_revision = '64743edb7fbb'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column(
        'punto_venta',
        'created_by',
        server_default=None,  
        existing_type=sa.String(length=255),
        nullable=True
    )


def downgrade():
    op.alter_column(
        'punto_venta',
        'created_by',
        server_default="system", 
        existing_type=sa.String(length=255),
        nullable=True
    )