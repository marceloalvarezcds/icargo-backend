
from datetime import datetime
from typing import Optional

from app.schemas.rounded_decimal_model import RoundedDecimal
from .estado_base_model import EstadoBaseModel


from pydantic import BaseModel



class MonedaCotizacion(EstadoBaseModel):
    id: int
    gestor_carga_id: int
    moneda_origen_id: int
    moneda_destino_id: int
    fecha: Optional[datetime] = None
    cotizacion_moneda: RoundedDecimal

    class Config:
        orm_mode = True
