

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.models import (
    MonedaCotizacion,
)
from app.enums import EstadoEnum

def read_cotizacion_moneda(db: Session, moneda_origen: int, moneda_destino:int, gestor_carga_id: int) -> MonedaCotizacion:

    sub_query = (
        db.query(
            #MonedaCotizacion.id,
            func.max(MonedaCotizacion.fecha).label("max_fecha"),
        )
        .filter(
            and_(
                MonedaCotizacion.moneda_origen_id == moneda_origen,
                MonedaCotizacion.moneda_destino_id == moneda_destino,  # Filtrar por gestor de carga específico
                MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
                MonedaCotizacion.gestor_carga_id == gestor_carga_id,
            )
        )
    ).subquery()

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
        .first()
    )