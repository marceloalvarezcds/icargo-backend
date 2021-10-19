from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import CentroOperativo, GestorCarga, GestorCargaCentroOperativo


def gestor_carga_centro_operativo_seeds(
    db: Session,
    centro_operativo: CentroOperativo,
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            GestorCargaCentroOperativo(
                centro_operativo_id=centro_operativo.id,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
