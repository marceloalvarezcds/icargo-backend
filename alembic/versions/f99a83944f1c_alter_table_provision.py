"""alter_table_provision

Revision ID: f99a83944f1c
Revises: 9d13debe4316
Create Date: 2025-05-26 15:53:01.677332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f99a83944f1c'
down_revision = '9d13debe4316'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("provision_anticipo_id_fkey", "provision", type_="foreignkey")
    op.drop_constraint("provision_complemento_id_fkey", "provision", type_="foreignkey")
    op.drop_constraint("provision_descuento_id_fkey", "provision", type_="foreignkey")

    op.drop_column( "provision", "anticipo_id" )

    op.create_foreign_key("provision_complemento_id_fkey", "provision", "orden_carga_complemento", ["complemento_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("provision_descuento_id_fkey", "provision", "orden_carga_descuento", ["descuento_id"], ["id"], ondelete="CASCADE")


def downgrade():
    op.add_column( "provision", "anticipo_id" )
    op.create_foreign_key("provision_anticipo_id_fkey", "provision", "orden_carga_anticipo_retirado", ["anticipo_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("provision_complemento_id_fkey", "provision", "orden_carga_complemento", ["complemento_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("provision_descuento_id_fkey", "provision", "orden_carga_descuento", ["descuento_id"], ["id"], ondelete="CASCADE")
