"""create comentarios_flota table

Revision ID: 6f0b76385ff4
Revises: 1853e3860b65
Create Date: 2025-07-16 08:48:15.341021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f0b76385ff4'
down_revision = '1853e3860b65'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comentarios_flota',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('comentable_type', sa.String(length=50), nullable=False),
        sa.Column('comentable_id', sa.Integer, nullable=False),
        sa.Column('comentario', sa.Text, nullable=False),
        sa.Column('tipo_evento', sa.String(length=100), nullable=True),
        sa.Column('archivo', sa.Text, nullable=True),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('modified_by', sa.String(length=255), nullable=True),
        sa.Column('modified_at', sa.TIMESTAMP, nullable=True),
        sa.Column('gestor_carga_id', sa.Integer, nullable=True),
        sa.ForeignKeyConstraint(['gestor_carga_id'], ['gestor_carga.id'], name='fk_comentarios_gestor')
    )



def downgrade():
    op.drop_table('comentarios_flota')

