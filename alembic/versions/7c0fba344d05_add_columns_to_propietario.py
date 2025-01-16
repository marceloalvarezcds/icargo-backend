"""add columns  to propietario

Revision ID: 7c0fba344d05
Revises: 752f99fc5688
Create Date: 2025-01-15 15:45:18.125297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c0fba344d05'
down_revision = '752f99fc5688'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('propietario_tipo_persona_id_fkey', 'propietario', type_='foreignkey')  
    op.drop_column('propietario', 'tipo_persona_id')  
    op.add_column('propietario', sa.Column('composicion_juridica_id', sa.Integer(), sa.ForeignKey('composicion_juridica.id'), nullable=True))
    op.add_column('propietario', sa.Column('tipo_documento_propietario_id', sa.Integer(), sa.ForeignKey('tipo_documento.id'), nullable=True))
    op.add_column('propietario', sa.Column('nombre_corto', sa.String(length=255), nullable=True))

def downgrade():
    op.add_column('propietario', sa.Column('tipo_persona_id', sa.Integer(), sa.ForeignKey('tipo_persona.id'), nullable=True))
    op.create_foreign_key('propietario_tipo_persona_id_fkey', 'propietario', 'tipo_persona', ['tipo_persona_id'], ['id'])
    op.drop_column('propietario', 'nombre_corto')
    op.drop_column('propietario', 'tipo_documento_propietario_id')
    op.drop_column('propietario', 'composicion_juridica_id')