from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Contacto, Proveedor, ProveedorContactoGestorCarga
from app.schemas import Cargo


def get_proveedor_contacto_gestor_carga_by(
    db: Session,
    cargo_id: int,
    proveedor_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[ProveedorContactoGestorCarga]:
    return (
        db.query(ProveedorContactoGestorCarga)
        .filter(
            ProveedorContactoGestorCarga.cargo_id == cargo_id,
            ProveedorContactoGestorCarga.proveedor_id == proveedor_id,
            ProveedorContactoGestorCarga.contacto_id == contacto_id,
            ProveedorContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_proveedor_contacto_gestor_carga(
    db: Session,
    cargo: Cargo,
    proveedor: Proveedor,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> ProveedorContactoGestorCarga:
    obj = ProveedorContactoGestorCarga(
        cargo_id=cargo.id,
        proveedor_id=proveedor.id,
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


def edit_proveedor_contacto_gestor_carga(
    obj: ProveedorContactoGestorCarga,
    db: Session,
    cargo: Cargo,
    proveedor: Proveedor,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> ProveedorContactoGestorCarga:
    obj.cargo_id = cargo.id
    obj.proveedor_id = proveedor.id
    obj.contacto_id = contacto.id
    obj.gestor_carga_id = gestor_carga_id
    obj.alias = alias
    obj.estado = EstadoEnum.ACTIVO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_proveedor_contacto_gestor_carga(db: Session, id: int, modified_by: str):
    obj = db.query(ProveedorContactoGestorCarga).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
