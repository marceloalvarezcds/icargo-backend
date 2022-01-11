from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .tipo_anticipo import TipoAnticipo
from .tipo_insumo import TipoInsumo


class FleteAnticipoForm(BaseModel):
    id: Optional[int] = None
    tipo_id: int
    tipo_descripcion: str
    tipo_insumo_id: Optional[int] = None
    tipo_insumo_descripcion: Optional[str] = None
    porcentaje: Decimal


class FleteAnticipo(FleteAnticipoForm):
    id: int
    tipo: TipoAnticipo
    tipo_insumo: Optional[TipoInsumo] = None
    flete_id: int
