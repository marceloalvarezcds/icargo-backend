from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaRemisionOrigen
from app.schemas import OrdenCargaRemisionOrigenForm


def get_orden_carga_remision_origen_list_by_orden_carga_id(
    db: Session, orden_carga_id: int
) -> List[OrdenCargaRemisionOrigen]:
    return (
        db.query(OrdenCargaRemisionOrigen)
        .filter(OrdenCargaRemisionOrigen.orden_carga_id == orden_carga_id)
        .order_by(OrdenCargaRemisionOrigen.created_by)
        .all()
    )


def get_orden_carga_remision_origen_by(
    db: Session,
    numero_documento: str,
) -> Optional[OrdenCargaRemisionOrigen]:
    return (
        db.query(OrdenCargaRemisionOrigen)
        .filter(OrdenCargaRemisionOrigen.numero_documento == numero_documento)
        .first()
    )


def get_orden_carga_remision_origen_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaRemisionOrigen]:
    return db.query(OrdenCargaRemisionOrigen).get(id)


def create_orden_carga_remision_origen(
    db: Session,
    data: OrdenCargaRemisionOrigenForm,
    foto_documento_url: str,
    modified_by: str,
) -> OrdenCargaRemisionOrigen:
    obj = OrdenCargaRemisionOrigen(
        numero_documento=data.numero_documento,
        fecha=data.fecha,
        cantidad=data.cantidad,
        unidad_id=data.unidad_id,
        foto_documento=foto_documento_url,
        orden_carga_id=data.orden_carga_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_remision_origen(
    obj: OrdenCargaRemisionOrigen,
    db: Session,
    data: OrdenCargaRemisionOrigenForm,
    foto_documento_url: Optional[str],
    modified_by: str,
) -> OrdenCargaRemisionOrigen:
    obj.numero_documento = data.numero_documento
    obj.fecha = data.fecha
    obj.cantidad = data.cantidad
    obj.unidad_id = data.unidad_id
    obj.orden_carga_id = data.orden_carga_id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    if foto_documento_url:
        obj.foto_documento = foto_documento_url
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga_remision_origen(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaRemisionOrigen).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
