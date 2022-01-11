from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .date_model import Date


class OrdenCargaRemisionDestinoForm(BaseModel):
    numero_documento: str
    cantidad: Decimal
    unidad_id: int
    foto_documento: Optional[str] = None
    numero_documento_origen: Optional[str] = None
    orden_carga_id: int


class OrdenCargaRemisionDestino(OrdenCargaRemisionDestinoForm):
    id: int
    fecha: Date
    unidad_abreviatura: str
    unidad_descripcion: str

    class Config:
        orm_mode = True
        use_enum_values = True
