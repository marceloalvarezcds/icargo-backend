
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.models import (
    MonedaCotizacion,
)
from app import repositories

def read_cotizacion_moneda(db: Session, moneda_origen: int, moneda_destino:int, gestor_carga_id: int) -> MonedaCotizacion:
    return repositories.get_ultima_cotizacion(db, moneda_origen, moneda_destino, gestor_carga_id)
