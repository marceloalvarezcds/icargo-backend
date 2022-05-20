from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import GestorCargaChofer


def get_gestor_carga_chofer_by(
    db: Session,
    chofer_id: int,
    gestor_carga_id: int,
) -> Optional[GestorCargaChofer]:
    return (
        db.query(GestorCargaChofer)
        .filter(
            GestorCargaChofer.chofer_id == chofer_id,
            GestorCargaChofer.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_gestor_carga_chofer(
    db: Session,
    chofer_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaChofer:
    obj = GestorCargaChofer(
        chofer_id=chofer_id,
        gestor_carga_id=gestor_carga_id,
        alias=alias,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_gestor_carga_chofer(
    obj: GestorCargaChofer,
    db: Session,
    chofer_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaChofer:
    obj.chofer_id = chofer_id
    obj.gestor_carga_id = gestor_carga_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.alias = alias
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
