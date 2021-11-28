from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Chofer, GestorCarga, GestorCargaChofer


def gestor_carga_chofer_seeds(
    db: Session,
    chofer: Chofer,
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            GestorCargaChofer(
                chofer_id=chofer.id,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
