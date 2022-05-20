from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Contacto, Remitente, RemitenteContactoGestorCarga
from app.schemas import Cargo


def get_remitente_contacto_gestor_carga_by(
    db: Session,
    remitente_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[RemitenteContactoGestorCarga]:
    return (
        db.query(RemitenteContactoGestorCarga)
        .filter(
            RemitenteContactoGestorCarga.remitente_id == remitente_id,
            RemitenteContactoGestorCarga.contacto_id == contacto_id,
            RemitenteContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def get_remitente_contacto_gestor_carga_by_cargo_id(
    db: Session,
    cargo_id: int,
    remitente_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[RemitenteContactoGestorCarga]:
    return (
        db.query(RemitenteContactoGestorCarga)
        .filter(
            RemitenteContactoGestorCarga.cargo_id == cargo_id,
            RemitenteContactoGestorCarga.remitente_id == remitente_id,
            RemitenteContactoGestorCarga.contacto_id == contacto_id,
            RemitenteContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def get_remitente_contacto_gestor_carga_by_id(
    db: Session,
    id: int,
) -> Optional[RemitenteContactoGestorCarga]:
    return db.query(RemitenteContactoGestorCarga).get(id)


def create_remitente_contacto_gestor_carga(
    db: Session,
    cargo: Cargo,
    remitente: Remitente,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> RemitenteContactoGestorCarga:
    obj = RemitenteContactoGestorCarga(
        cargo_id=cargo.id,
        remitente_id=remitente.id,
        contacto_id=contacto.id,
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


def edit_remitente_contacto_gestor_carga(
    obj: RemitenteContactoGestorCarga,
    db: Session,
    cargo: Cargo,
    remitente: Remitente,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> RemitenteContactoGestorCarga:
    obj.cargo_id = cargo.id
    obj.remitente_id = remitente.id
    obj.contacto_id = contacto.id
    obj.gestor_carga_id = gestor_carga_id
    obj.alias = alias
    obj.estado = EstadoEnum.ACTIVO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_remitente_contacto_gestor_carga(db: Session, id: int, modified_by: str):
    obj = db.query(RemitenteContactoGestorCarga).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
