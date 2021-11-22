from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import GestorCarga, GestorCargaPropietario, Propietario


def gestor_carga_propietario_seeds(
    db: Session,
    propietario: Propietario,
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            GestorCargaPropietario(
                propietario_id=propietario.id,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
