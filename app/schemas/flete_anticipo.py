from typing import Optional

from pydantic import BaseModel

from app.schemas.rounded_decimal_model import RoundedDecimal

from .tipo_anticipo import TipoAnticipo
from .tipo_insumo import TipoInsumo


class FleteAnticipoForm(BaseModel):
    id: Optional[int] = None
    tipo_id: int
    tipo_descripcion: str
    tipo_insumo_id: Optional[int] = None
    tipo_insumo_descripcion: Optional[str] = None
    porcentaje: Optional[RoundedDecimal] = None
    concepto: Optional[str] = None


class FleteAnticipo(FleteAnticipoForm):
    id: int
    tipo: TipoAnticipo
    tipo_insumo: Optional[TipoInsumo] = None
    concepto: str
    flete_id: int

    class Config:
        orm_mode = True
