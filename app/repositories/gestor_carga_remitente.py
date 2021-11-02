from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import GestorCargaRemitente


def get_gestor_carga_remitente_by(
    db: Session,
    remitente_id: int,
    gestor_carga_id: int,
) -> Optional[GestorCargaRemitente]:
    return (
        db.query(GestorCargaRemitente)
        .filter(
            GestorCargaRemitente.remitente_id == remitente_id,
            GestorCargaRemitente.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_gestor_carga_remitente(
    db: Session,
    remitente_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaRemitente:
    obj = GestorCargaRemitente(
        remitente_id=remitente_id,
        gestor_carga_id=gestor_carga_id,
        alias=alias,
        estado=EstadoEnum.ACTIVO.value,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_gestor_carga_remitente(
    obj: GestorCargaRemitente,
    db: Session,
    remitente_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaRemitente:
    obj.remitente_id = remitente_id
    obj.gestor_carga_id = gestor_carga_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.alias = alias
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
