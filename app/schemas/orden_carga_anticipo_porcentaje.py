from typing import Optional

from pydantic import BaseModel

from app.schemas.rounded_decimal_model import RoundedDecimal

from .flete_anticipo import FleteAnticipo
from .tipo_anticipo import TipoAnticipo
from .tipo_insumo import TipoInsumo


class OrdenCargaAnticipoPorcentajeForm(BaseModel):
    flete_anticipo_id: int
    orden_carga_id: int
    porcentaje: Optional[RoundedDecimal] = None
    porcentaje_minimo: Optional[RoundedDecimal] = None


class OrdenCargaAnticipoPorcentaje(OrdenCargaAnticipoPorcentajeForm):
    id: int
    porcentaje: RoundedDecimal
    porcentaje_minimo: RoundedDecimal
    flete_anticipo: FleteAnticipo
    tipo_id: int
    tipo: TipoAnticipo
    tipo_descripcion: str
    tipo_insumo_id: Optional[int] = None
    tipo_insumo: Optional[TipoInsumo] = None
    tipo_insumo_descripcion: Optional[str] = None
    concepto: str
    flete_id: int

    class Config:
        orm_mode = True
