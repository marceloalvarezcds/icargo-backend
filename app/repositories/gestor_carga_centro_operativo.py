from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import GestorCargaCentroOperativo


def get_gestor_carga_centro_operativo_by(
    db: Session,
    centro_operativo_id: int,
    gestor_carga_id: int,
) -> Optional[GestorCargaCentroOperativo]:
    return (
        db.query(GestorCargaCentroOperativo)
        .filter(
            GestorCargaCentroOperativo.centro_operativo_id == centro_operativo_id,
            GestorCargaCentroOperativo.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_gestor_carga_centro_operativo(
    db: Session,
    centro_operativo_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaCentroOperativo:
    obj = GestorCargaCentroOperativo(
        centro_operativo_id=centro_operativo_id,
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


def edit_gestor_carga_centro_operativo(
    obj: GestorCargaCentroOperativo,
    db: Session,
    centro_operativo_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaCentroOperativo:
    obj.centro_operativo_id = centro_operativo_id
    obj.gestor_carga_id = gestor_carga_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.alias = alias
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
