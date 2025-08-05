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

    orden_carga = db.query(OrdenCarga).filter_by(id=data.orden_carga_id).first()
    if not orden_carga or not orden_carga.flete_id:
        return obj

    flete = db.query(Flete).filter_by(id=orden_carga.flete_id).first()
    if not flete:
        return obj

    saldo_inicial = flete.condicion_cantidad
    print(f"Saldo inicial (condición cantidad): {saldo_inicial}")

    unidad = db.query(Unidad).filter_by(id=data.unidad_id).first()
    factor = unidad.conversion_kg if unidad and unidad.conversion_kg else Decimal("1")
    cantidad_en_kg = data.cantidad * factor
    print(f"Cantidad en kg enviada ahora: {cantidad_en_kg}")

    # Total remisionado acumulado en todas las OCs del flete (kg)
    total_remisionado_flete = (
        db.query(func.sum(OrdenCargaRemisionOrigen.cantidad * Unidad.conversion_kg))
        .join(OrdenCarga, OrdenCarga.id == OrdenCargaRemisionOrigen.orden_carga_id)
        .join(Unidad, OrdenCargaRemisionOrigen.unidad_id == Unidad.id)
        .filter(OrdenCarga.flete_id == flete.id)
        .scalar()
    ) or Decimal("0")
    print(f"Total remisionado acumulado flete (kg): {total_remisionado_flete}")

    diferencia = saldo_inicial - total_remisionado_flete
    print(f"Diferencia saldo_inicial - total_remisionado_flete: {diferencia}")

    flete.saldo = diferencia
    flete.cargado = total_remisionado_flete
    print(f"Saldo actualizado: {flete.saldo}")
    print(f"Cargado actualizado: {flete.cargado}")

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
    unidad_anterior = db.query(Unidad).filter_by(id=obj.unidad_id).first()
    factor_anterior = unidad_anterior.conversion_kg if unidad_anterior else Decimal("1")
    cantidad_anterior_convertida = Decimal(obj.cantidad) * factor_anterior

    unidad_nueva = db.query(Unidad).filter_by(id=data.unidad_id).first()
    factor_nuevo = unidad_nueva.conversion_kg if unidad_nueva else Decimal("1")
    cantidad_nueva_convertida = Decimal(data.cantidad) * factor_nuevo

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

    orden_carga = db.query(OrdenCarga).filter_by(id=data.orden_carga_id).first()
    if not orden_carga or not orden_carga.flete_id:
        return obj

    flete = db.query(Flete).filter_by(id=orden_carga.flete_id).first()
    if not flete:
        return obj

    saldo_inicial = flete.condicion_cantidad

    # Recalcular total remisionado acumulado para el flete
    total_remisionado_flete = (
        db.query(func.sum(OrdenCargaRemisionOrigen.cantidad * Unidad.conversion_kg))
        .join(OrdenCarga, OrdenCargaRemisionOrigen.orden_carga_id == OrdenCarga.id)
        .join(Unidad, OrdenCargaRemisionOrigen.unidad_id == Unidad.id)
        .filter(OrdenCarga.flete_id == flete.id)
        .scalar()
    ) or Decimal("0")

    flete.saldo = saldo_inicial - total_remisionado_flete
    flete.cargado = total_remisionado_flete

    db.add(flete)
    db.commit()

    return obj


def delete_orden_carga_remision_origen(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaRemisionOrigen).get(id)
    if not obj:
        print("Remisión no encontrada")
        return None

    print(f"Eliminando remisión con ID: {id}")
    print(f"Cantidad de la remisión: {obj.cantidad}, Unidad ID: {obj.unidad_id}")

    # Actualizar auditoría
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()

    orden_carga = db.query(OrdenCarga).filter_by(id=obj.orden_carga_id).first()
    if not orden_carga or not orden_carga.flete_id:
        print("Orden de carga sin flete, eliminando remisión")
        db.delete(obj)
        db.commit()
        return

    flete = db.query(Flete).filter_by(id=orden_carga.flete_id).first()
    if not flete:
        print("Flete no encontrado, eliminando remisión")
        db.delete(obj)
        db.commit()
        return

    db.delete(obj)
    db.commit()
    print("Remisión eliminada")

    cantidad_nominada_oc = orden_carga.cantidad_nominada or Decimal("0")
    print(f"Cantidad nominada de la OC: {cantidad_nominada_oc}")

    # Verificar si quedan otras remisiones
    remisiones_restantes = (
        db.query(OrdenCargaRemisionOrigen)
        .join(OrdenCarga, OrdenCargaRemisionOrigen.orden_carga_id == OrdenCarga.id)
        .filter(OrdenCarga.flete_id == flete.id)
        .all()
    )

    if not remisiones_restantes:
        print("No quedan remisiones, restaurando valores del flete")
        flete.cargado = cantidad_nominada_oc
        flete.saldo = flete.condicion_cantidad - cantidad_nominada_oc
    else:
        print(f"Recalculando remisiones restantes ({len(remisiones_restantes)})")
        total_remisionado_flete = (
            db.query(func.sum(OrdenCargaRemisionOrigen.cantidad * Unidad.conversion_kg))
            .join(OrdenCarga, OrdenCargaRemisionOrigen.orden_carga_id == OrdenCarga.id)
            .join(Unidad, OrdenCargaRemisionOrigen.unidad_id == Unidad.id)
            .filter(OrdenCarga.flete_id == flete.id)
            .scalar()
        ) or Decimal("0")

        print(f"Total remisionado restante en kg: {total_remisionado_flete}")
        flete.cargado = total_remisionado_flete
        flete.saldo = cantidad_nominada_oc - total_remisionado_flete

    print(f"Flete actualizado - Cargado: {flete.cargado}, Saldo: {flete.saldo}")
    db.add(flete)
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
