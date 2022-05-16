from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Contacto, Propietario, PropietarioContactoGestorCarga
from app.schemas import Cargo


def get_propietario_contacto_gestor_carga_by(
    db: Session,
    propietario_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[PropietarioContactoGestorCarga]:
    return (
        db.query(PropietarioContactoGestorCarga)
        .filter(
            PropietarioContactoGestorCarga.propietario_id == propietario_id,
            PropietarioContactoGestorCarga.contacto_id == contacto_id,
            PropietarioContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def get_propietario_contacto_gestor_carga_by_cargo_id(
    db: Session,
    cargo_id: int,
    propietario_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[PropietarioContactoGestorCarga]:
    return (
        db.query(PropietarioContactoGestorCarga)
        .filter(
            PropietarioContactoGestorCarga.cargo_id == cargo_id,
            PropietarioContactoGestorCarga.propietario_id == propietario_id,
            PropietarioContactoGestorCarga.contacto_id == contacto_id,
            PropietarioContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_propietario_contacto_gestor_carga(
    db: Session,
    cargo: Cargo,
    propietario: Propietario,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> PropietarioContactoGestorCarga:
    obj = PropietarioContactoGestorCarga(
        cargo_id=cargo.id,
        propietario_id=propietario.id,
        contacto_id=contacto.id,
        gestor_carga_id=gestor_carga_id,
        alias=alias,
        estado=EstadoEnum.ACTIVO.value,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_propietario_contacto_gestor_carga(
    obj: PropietarioContactoGestorCarga,
    db: Session,
    cargo: Cargo,
    propietario: Propietario,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> PropietarioContactoGestorCarga:
    obj.cargo_id = cargo.id
    obj.propietario_id = propietario.id
    obj.contacto_id = contacto.id
    obj.gestor_carga_id = gestor_carga_id
    obj.alias = alias
    obj.estado = EstadoEnum.ACTIVO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_propietario_contacto_gestor_carga(db: Session, id: int, modified_by: str):
    obj = db.query(PropietarioContactoGestorCarga).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
