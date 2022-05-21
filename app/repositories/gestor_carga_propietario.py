from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import GestorCargaPropietario


def get_gestor_carga_propietario_by(
    db: Session,
    propietario_id: int,
    gestor_carga_id: int,
) -> Optional[GestorCargaPropietario]:
    return (
        db.query(GestorCargaPropietario)
        .filter(
            GestorCargaPropietario.propietario_id == propietario_id,
            GestorCargaPropietario.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_gestor_carga_propietario(
    db: Session,
    propietario_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaPropietario:
    obj = GestorCargaPropietario(
        propietario_id=propietario_id,
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


def edit_gestor_carga_propietario(
    obj: GestorCargaPropietario,
    db: Session,
    propietario_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaPropietario:
    obj.propietario_id = propietario_id
    obj.gestor_carga_id = gestor_carga_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.alias = alias
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
