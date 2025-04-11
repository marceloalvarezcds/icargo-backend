from typing import Optional
from pydantic import BaseModel
from .rounded_decimal_model import RoundedDecimal
from .moneda import Moneda


class MonedaCotizacion(BaseModel):
    id: int
    gestor_carga_id: int
    moneda_origen_id: int
    moneda_destino_id: int
    #moneda: Moneda
    fecha: str
    estado: str
    cotizacion_moneda: RoundedDecimal

    class Config:
        orm_mode = True
