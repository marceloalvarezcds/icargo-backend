"""Added product_detail table relationship

Revision ID: 488433d129c3
Revises: 1d1897aa2b6d
Create Date: 2021-04-22 22:55:54.310847

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '488433d129c3'
down_revision = '1d1897aa2b6d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product_detail',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('product_id', sa.Integer, sa.ForeignKey("product.id")),
                    sa.Column('description', sa.String))


def downgrade():
    op.drop_table('product_detail')
