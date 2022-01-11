from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaRemisionDestino
from app.schemas import OrdenCargaRemisionDestinoForm


def get_orden_carga_remision_destino_by(
    db: Session,
    numero_documento: str,
) -> Optional[OrdenCargaRemisionDestino]:
    return (
        db.query(OrdenCargaRemisionDestino)
        .filter(OrdenCargaRemisionDestino.numero_documento == numero_documento)
        .first()
    )


def get_orden_carga_remision_destino_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaRemisionDestino]:
    return db.query(OrdenCargaRemisionDestino).get(id)


def create_orden_carga_remision_destino(
    db: Session,
    data: OrdenCargaRemisionDestinoForm,
    foto_documento_url: str,
    modified_by: str,
) -> OrdenCargaRemisionDestino:
    obj = OrdenCargaRemisionDestino(
        numero_documento=data.numero_documento,
        cantidad=data.cantidad,
        unidad_id=data.unidad_id,
        foto_documento=foto_documento_url,
        numero_documento_origen=data.numero_documento_origen,
        orden_carga_id=data.orden_carga_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_remision_destino(
    obj: OrdenCargaRemisionDestino,
    db: Session,
    data: OrdenCargaRemisionDestinoForm,
    foto_documento_url: Optional[str],
    modified_by: str,
) -> OrdenCargaRemisionDestino:
    obj.numero_documento = data.numero_documento
    obj.cantidad = data.cantidad
    obj.unidad_id = data.unidad_id
    obj.foto_documento = foto_documento_url
    obj.numero_documento_origen = data.numero_documento_origen
    obj.orden_carga_id = data.orden_carga_id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga_remision_destino(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaRemisionDestino).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
