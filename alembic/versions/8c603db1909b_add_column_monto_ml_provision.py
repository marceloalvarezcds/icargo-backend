"""add_column_monto_ml_provision

Revision ID: 8c603db1909b
Revises: ec2d6cec5741
Create Date: 2025-06-18 16:36:34.216353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c603db1909b'
down_revision = 'ec2d6cec5741'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "provision",
        sa.Column(
            "monto_mon_local", sa.Numeric(precision=38, scale=10), nullable=True
        ),
    )


def downgrade():
    op.drop_column("provision", "monto_mon_local")
