from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Contacto, PuntoVenta, PuntoVentaContactoGestorCarga
from app.schemas import Cargo


def get_punto_venta_contacto_gestor_carga_by(
    db: Session,
    cargo_id: int,
    punto_venta_id: int,
    contacto_id: int,
    gestor_carga_id: int,
) -> Optional[PuntoVentaContactoGestorCarga]:
    return (
        db.query(PuntoVentaContactoGestorCarga)
        .filter(
            PuntoVentaContactoGestorCarga.cargo_id == cargo_id,
            PuntoVentaContactoGestorCarga.punto_venta_id == punto_venta_id,
            PuntoVentaContactoGestorCarga.contacto_id == contacto_id,
            PuntoVentaContactoGestorCarga.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_punto_venta_contacto_gestor_carga(
    db: Session,
    cargo: Cargo,
    punto_venta: PuntoVenta,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> PuntoVentaContactoGestorCarga:
    obj = PuntoVentaContactoGestorCarga(
        cargo_id=cargo.id,
        punto_venta_id=punto_venta.id,
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


def edit_punto_venta_contacto_gestor_carga(
    obj: PuntoVentaContactoGestorCarga,
    db: Session,
    cargo: Cargo,
    punto_venta: PuntoVenta,
    contacto: Contacto,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> PuntoVentaContactoGestorCarga:
    obj.cargo_id = cargo.id
    obj.punto_venta_id = punto_venta.id
    obj.contacto_id = contacto.id
    obj.gestor_carga_id = gestor_carga_id
    obj.alias = alias
    obj.estado = EstadoEnum.ACTIVO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_punto_venta_contacto_gestor_carga(db: Session, id: int, modified_by: str):
    obj = db.query(PuntoVentaContactoGestorCarga).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
