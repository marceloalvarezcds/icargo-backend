"""Added tags table and reacreated relationship

Revision ID: 4ad3f83a84f0
Revises: 488433d129c3
Create Date: 2021-04-24 18:27:22.826087

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4ad3f83a84f0'
down_revision = '488433d129c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tag',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('name', sa.String(100), nullable=False),
                    sa.Column('description', sa.String(250), nullable=False))

    op.create_table('product_tag',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('product_id', sa.Integer, sa.ForeignKey("product.id")),
                    sa.Column('tag_id', sa.Integer, sa.ForeignKey("tag.id")))


def downgrade():
    op.drop_table('tag')
    op.drop_table('product_tag')
