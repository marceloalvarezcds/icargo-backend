"""Remove unique constraint from numero_documento in remision origen y destino

Revision ID: cb4e1cb888ce
Revises: e012f3391dab
Create Date: 2025-07-14 07:42:13.604110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb4e1cb888ce'
down_revision = 'e012f3391dab'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('orden_carga_remision_origen_numero_documento_key', 'orden_carga_remision_origen', type_='unique')
    op.drop_constraint('orden_carga_remision_destino_numero_documento_key', 'orden_carga_remision_destino', type_='unique')

def downgrade():
    op.create_unique_constraint('orden_carga_remision_origen_numero_documento_key', 'orden_carga_remision_origen', ['numero_documento'])
    op.create_unique_constraint('orden_carga_remision_destino_numero_documento_key', 'orden_carga_remision_destino', ['numero_documento'])
