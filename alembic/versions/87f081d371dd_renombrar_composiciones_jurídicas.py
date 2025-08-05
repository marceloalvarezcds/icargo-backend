"""Renombrar composiciones jurídicas

Revision ID: 87f081d371dd
Revises: af412c910127
Create Date: 2025-07-21 13:56:50.775029

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String

# revision identifiers, used by Alembic.
revision = '87f081d371dd'
down_revision = 'af412c910127'
branch_labels = None
depends_on = None


def upgrade():
    composicion_juridica = table(
        "composicion_juridica",
        column("nombre", String),
    )

    op.execute(
        composicion_juridica.update()
        .where(composicion_juridica.c.nombre == "Sociedad de Responsabilidad Limitada - S.A.C.I.")
        .values(nombre="Sociedad de Responsabilidad Limitada - S.R.L.")
    )

    op.execute(
        composicion_juridica.update()
        .where(composicion_juridica.c.nombre == "Sociedad Anónima Comercial Industrial - S.R.L.")
        .values(nombre="Sociedad Anónima Comercial Industrial - S.A.C.I.")
    )


def downgrade():

    composicion_juridica = table(
        "composicion_juridica",
        column("nombre", String),
    )

    op.execute(
        composicion_juridica.update()
        .where(composicion_juridica.c.nombre == "Sociedad de Responsabilidad Limitada - S.R.L.")
        .values(nombre="Sociedad de Responsabilidad Limitada - S.A.C.I.")
    )

    op.execute(
        composicion_juridica.update()
        .where(composicion_juridica.c.nombre == "Sociedad Anónima Comercial Industrial - S.A.C.I.")
        .values(nombre="Sociedad Anónima Comercial Industrial - S.R.L.")
    )
