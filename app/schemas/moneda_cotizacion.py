<<<<<<< HEAD
from datetime import datetime
from typing import Optional

from app.schemas.rounded_decimal_model import RoundedDecimal
from .estado_base_model import EstadoBaseModel


class MonedaCotizacion(EstadoBaseModel):
=======
from typing import Optional
from pydantic import BaseModel
from .rounded_decimal_model import RoundedDecimal
from .moneda import Moneda


class MonedaCotizacion(BaseModel):
>>>>>>> 3a4c593dbb1a6973b45b3727d4cd7fbb0f3981c8
    id: int
    gestor_carga_id: int
    moneda_origen_id: int
    moneda_destino_id: int
<<<<<<< HEAD
    fecha: Optional[datetime] = None
=======
    #moneda: Moneda
    fecha: str
    estado: str
>>>>>>> 3a4c593dbb1a6973b45b3727d4cd7fbb0f3981c8
    cotizacion_moneda: RoundedDecimal

    class Config:
        orm_mode = True
