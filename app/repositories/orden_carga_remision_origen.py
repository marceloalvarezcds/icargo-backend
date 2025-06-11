from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaRemisionOrigen
from app.models.flete import Flete
from app.models.orden_carga import OrdenCarga
from app.models.unidad import Unidad
from app.schemas import OrdenCargaRemisionOrigenForm
from app.logger import logger
from sqlalchemy import func
from decimal import Decimal

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
    foto_documento_url: Optional[str],
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

    orden_carga = db.query(OrdenCarga).filter(OrdenCarga.id == data.orden_carga_id).first()
    if orden_carga and orden_carga.flete_id:
        flete = db.query(Flete).filter(Flete.id == orden_carga.flete_id).first()

        # 🔹 1. Obtener la unidad y factor de conversión como Decimal
        unidad = db.query(Unidad).filter(Unidad.id == data.unidad_id).first()
        factor = unidad.conversion_kg if unidad and unidad.conversion_kg else Decimal("1")

        # 🔹 2. Convertir cantidad a kg como Decimal
        cantidad_convertida = Decimal(data.cantidad) * factor

        if flete:
            # 🔹 3. Calcular diferencia con la cantidad nominada (Decimal - Decimal)
            diferencia = orden_carga.cantidad_nominada - cantidad_convertida
            flete.saldo += diferencia

            # 🔹 4. Calcular el total remisionado en kg
            total_remisionado = (
                db.query(func.sum(OrdenCargaRemisionOrigen.cantidad * Unidad.conversion_kg))
                .join(OrdenCarga, OrdenCargaRemisionOrigen.orden_carga_id == OrdenCarga.id)
                .join(Unidad, OrdenCargaRemisionOrigen.unidad_id == Unidad.id)
                .filter(OrdenCarga.flete_id == flete.id)
                .scalar()
            ) or Decimal("0")

            flete.cargado = total_remisionado
            db.add(flete)
            db.commit()

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


def get_remision_origen_list_by_nro_remito(
    db: Session, nro_remito: Optional[str] = None
) -> List[OrdenCargaRemisionOrigen]:

    if nro_remito:
        return (
            db.query(OrdenCargaRemisionOrigen)
            .filter(OrdenCargaRemisionOrigen.numero_documento.like(('%'+nro_remito+'%')))
            .order_by(OrdenCargaRemisionOrigen.created_by)
            .all()
        )
    else:
        return (
            db.query(OrdenCargaRemisionOrigen)
            .order_by(OrdenCargaRemisionOrigen.created_by)
            .all()
        )
