"""Added product table

Revision ID: f9e0454aac60
Revises: 029d7e5d1089
Create Date: 2021-04-21 02:37:24.093417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9e0454aac60'
down_revision = '029d7e5d1089'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('name', sa.String(120), nullable=False),
                    sa.Column('price', sa.Float),
                    sa.Column('brand', sa.String),
                    sa.Column('status', sa.Enum('out_of_stock', 'in_stock', 'running_low', name='product_status',
                                                nullable=False)))


def downgrade():
    op.drop_table('product')
