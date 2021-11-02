from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import GestorCarga, GestorCargaRemitente, Remitente


def gestor_carga_remitente_seeds(
    db: Session,
    remitente: Remitente,
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            GestorCargaRemitente(
                remitente_id=remitente.id,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
