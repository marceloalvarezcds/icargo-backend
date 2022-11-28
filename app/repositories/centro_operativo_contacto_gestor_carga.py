from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import CentroOperativo, CentroOperativoContactoGestorCarga, Contacto
from app.schemas import Cargo


def get_centro_operativo_contacto_gestor_carga_by(
    db: Session,
    centro_operativo_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[CentroOperativoContactoGestorCarga]:
    return (
        db.query(CentroOperativoContactoGestorCarga)
        .filter(
            CentroOperativoContactoGestorCarga.centro_operativo_id
            == centro_operativo_id,
            CentroOperativoContactoGestorCarga.contacto_id == contacto_id,
            CentroOperativoContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def get_centro_operativo_contacto_gestor_carga_by_cargo_id(
    db: Session,
    cargo_id: int,
    centro_operativo_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[CentroOperativoContactoGestorCarga]:
    return (
        db.query(CentroOperativoContactoGestorCarga)
        .filter(
            CentroOperativoContactoGestorCarga.cargo_id == cargo_id,
            CentroOperativoContactoGestorCarga.centro_operativo_id
            == centro_operativo_id,
            CentroOperativoContactoGestorCarga.contacto_id == contacto_id,
            CentroOperativoContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def get_centro_operativo_contacto_gestor_carga_by_id(
    db: Session,
    id: int,
) -> Optional[CentroOperativoContactoGestorCarga]:
    return db.query(CentroOperativoContactoGestorCarga).get(id)


def create_centro_operativo_contacto_gestor_carga(
    db: Session,
    cargo: Cargo,
    centro_operativo: CentroOperativo,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: Optional[str],
    modified_by: str,
) -> CentroOperativoContactoGestorCarga:
    obj = CentroOperativoContactoGestorCarga(
        cargo_id=cargo.id,
        centro_operativo_id=centro_operativo.id,
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


def edit_centro_operativo_contacto_gestor_carga(
    obj: CentroOperativoContactoGestorCarga,
    db: Session,
    cargo: Cargo,
    centro_operativo: CentroOperativo,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: Optional[str],
    modified_by: str,
) -> CentroOperativoContactoGestorCarga:
    obj.cargo_id = cargo.id
    obj.centro_operativo_id = centro_operativo.id
    obj.contacto_id = contacto.id
    obj.gestor_carga_id = gestor_carga_id
    obj.alias = alias
    obj.estado = EstadoEnum.ACTIVO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_centro_operativo_contacto_gestor_carga(
    db: Session, id: int, modified_by: str
):
    obj = db.query(CentroOperativoContactoGestorCarga).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
