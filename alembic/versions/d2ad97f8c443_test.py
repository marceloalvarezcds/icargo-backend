"""test

Revision ID: d2ad97f8c443
Revises: 59c07cc016f2
Create Date: 2024-09-25 07:21:50.815340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2ad97f8c443'
down_revision = '59c07cc016f2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    "test",
    sa.Column(
        "modified_by", sa.String(length=255), server_default="system", nullable=True
        ),
    )

def downgrade():
    op.drop_table("test")
