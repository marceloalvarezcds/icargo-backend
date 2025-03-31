
from sqlalchemy.orm import Session  # type: ignore

from app.enums.estado import EstadoEnum
from app.models.moneda_cotizacion import MonedaCotizacion


def get_cotizacion_by_moneda(db: Session, moneda_origen_id: int, moneda_destino_id: int):
    cotizacion = (
        db.query(MonedaCotizacion)
        .filter(
            MonedaCotizacion.moneda_origen_id == moneda_origen_id,
            MonedaCotizacion.moneda_destino_id == moneda_destino_id,
            MonedaCotizacion.estado == EstadoEnum.ACTIVO.value
        )
        .order_by(MonedaCotizacion.fecha.desc())  # Obtener la más reciente
        .first()
    )
    return cotizacion  # Retorna la cotización obtenida

