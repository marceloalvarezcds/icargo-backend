from typing import List, Optional
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from app.models import MonedaCotizacion
from app.enums import EstadoEnum

def get_moneda_cotizacion_by_id(db: Session, id: int) -> Optional[MonedaCotizacion]:
    return db.query(MonedaCotizacion).get(id)


def get_moneda_cotizacion_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[MonedaCotizacion]:
    return (
        db.query(MonedaCotizacion)
        .filter(
            and_(
                MonedaCotizacion.gestor_carga_id == gestor_carga_id,
                MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
            )
        )
        .order_by(MonedaCotizacion.id.desc())
        .all()
    )


def get_max_date_cotizacio_by_origen_destino(db: Session, origen_id: int, destino_id: int, gestor_carga_id: int):
    return (
        db.query(
            func.max(MonedaCotizacion.fecha).label("max_fecha"),
        )
        .filter(
            and_(
                MonedaCotizacion.moneda_origen_id == origen_id,
                MonedaCotizacion.moneda_destino_id == destino_id,  # Filtrar por gestor de carga específico
                MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
                MonedaCotizacion.gestor_carga_id == gestor_carga_id,
            )
        )
    )


def get_ultima_cotizacion_query(db: Session, moneda_origen: int, moneda_destino:int, gestor_carga_id: int) -> MonedaCotizacion:
    sub_query = get_max_date_cotizacio_by_origen_destino(db, moneda_origen, moneda_destino, gestor_carga_id).subquery()
    return (
        db.query(MonedaCotizacion)
        .join(
            sub_query,
            and_(
                sub_query.c.max_fecha == MonedaCotizacion.fecha,
            ),
        )
        .filter(
            and_(
                MonedaCotizacion.moneda_origen_id == moneda_origen,
                MonedaCotizacion.moneda_destino_id == moneda_destino,  # Filtrar por gestor de carga específico
                MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
                MonedaCotizacion.gestor_carga_id == gestor_carga_id,
            )
        )
    )

def get_ultima_cotizacion(db: Session, moneda_origen: int, moneda_destino:int, gestor_carga_id: int) -> MonedaCotizacion:
    query = get_ultima_cotizacion_query(db, moneda_origen, moneda_destino, gestor_carga_id)
    return query.first()
