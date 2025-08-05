
from datetime import date, datetime
from typing import Optional

from app.enums.estado import EstadoEnum
from app.schemas.rounded_decimal_model import RoundedDecimal
from .estado_base_model import EstadoBaseModel


from pydantic import BaseModel

class MonedaCotizacionForm(BaseModel):
    gestor_carga_id: int
    moneda_origen_id: int
    moneda_destino_id: int
    fecha: Optional[date] = None
    cotizacion_moneda: Optional[RoundedDecimal]

class MonedaCotizacion(BaseModel):
    id: int
    gestor_carga_id: int
    moneda_origen_id: int
    moneda_destino_id: int
    fecha: Optional[date] = None
    estado: EstadoEnum
    #fecha: str
    cotizacion_moneda: Optional[RoundedDecimal]
    gestor_carga_nombre: Optional[str] = None
    moneda_origen_nombre: Optional[str] = None
    moneda_destino_nombre: Optional[str] = None
    class Config:
        orm_mode = True
        use_enum_values = True

