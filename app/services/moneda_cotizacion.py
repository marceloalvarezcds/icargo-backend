
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.enums.estado import EstadoEnum
from app.models import (
    MonedaCotizacion,
)
from app import repositories

def read_cotizacion_moneda(db: Session, moneda_origen: int, moneda_destino: int, gestor_carga_id: int) -> MonedaCotizacion:
    # Delegar la lógica de la consulta al repositorio
    return repositories.get_ultima_cotizacion(db, moneda_origen, moneda_destino, gestor_carga_id)

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
