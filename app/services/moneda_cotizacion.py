
from typing import Optional
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.enums.estado import EstadoEnum
from fastapi import HTTPException, status
from app.models import (
    MonedaCotizacion,
)
from app import repositories
from app.schemas.moneda_cotizacion import MonedaCotizacionForm
from app.utils.gestor_carga import get_gestor_carga_by_params

def read_cotizacion_moneda(db: Session, moneda_origen: int, moneda_destino: int, gestor_carga_id: int) -> MonedaCotizacion:
    return repositories.get_ultima_cotizacion(db, moneda_origen, moneda_destino, gestor_carga_id)

def get_moneda_cotizacion_by_id(db: Session, id: int) -> MonedaCotizacion:
    obj = repositories.get_moneda_cotizacion_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return obj

def get_cotizacion_moneda(db: Session, moneda_id: int, gestor_carga_id: int) -> MonedaCotizacion:
    resultado = (
        db.query(MonedaCotizacion)
        .filter(
            MonedaCotizacion.moneda_origen_id == moneda_id,
            MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
            MonedaCotizacion.gestor_carga_id == gestor_carga_id,
        )
        .order_by(MonedaCotizacion.fecha.desc())
        .first()
    )
    return resultado


def update_moneda_cotizacion_by_gestor_moneda_fecha(
    db: Session,
    data: MonedaCotizacionForm,
    modified_by: str,
) -> MonedaCotizacion:
    from datetime import datetime
    from fastapi import HTTPException, status

    fecha = data.fecha.date() if isinstance(data.fecha, datetime) else data.fecha

    # Buscar si ya existe una cotización para esa fecha + gestor + monedas
    existing = db.query(MonedaCotizacion).filter(
        MonedaCotizacion.gestor_carga_id == data.gestor_carga_id,
        MonedaCotizacion.moneda_origen_id == data.moneda_origen_id,
        MonedaCotizacion.moneda_destino_id == data.moneda_destino_id,
        MonedaCotizacion.fecha == fecha,
    ).first()

    if existing:
        if existing.cotizacion_moneda == data.cotizacion_moneda:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cotización con la misma fecha, monedas y valor."
            )
        # Solo actualiza si la fecha es la misma pero cambia el valor
        existing.cotizacion_moneda = data.cotizacion_moneda
        existing.modified_by = modified_by
        db.commit()
        db.refresh(existing)
        return existing

    # Si la fecha cambió, inactivar cotizaciones activas previas con misma combinación
    cotizaciones_activas = db.query(MonedaCotizacion).filter(
        MonedaCotizacion.gestor_carga_id == data.gestor_carga_id,
        MonedaCotizacion.moneda_origen_id == data.moneda_origen_id,
        MonedaCotizacion.moneda_destino_id == data.moneda_destino_id,
        MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
    ).all()

    for cot in cotizaciones_activas:
        cot.estado = EstadoEnum.INACTIVO.value
        cot.modified_by = modified_by
    db.flush()
    # Crear nueva cotización activa
    nueva_cotizacion = MonedaCotizacion(
        gestor_carga_id=data.gestor_carga_id,
        moneda_origen_id=data.moneda_origen_id,
        moneda_destino_id=data.moneda_destino_id,
        fecha=fecha,
        cotizacion_moneda=data.cotizacion_moneda,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )

    db.add(nueva_cotizacion)
    db.commit()
    db.refresh(nueva_cotizacion)
    return nueva_cotizacion







