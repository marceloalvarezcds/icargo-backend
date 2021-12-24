from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .tipo_anticipo import TipoAnticipo


class FleteAnticipoForm(BaseModel):
    id: Optional[int] = None
    tipo_id: int
    tipo_descripcion: str
    porcentaje: Decimal


class FleteAnticipo(FleteAnticipoForm):
    id: int
    tipo: TipoAnticipo
    flete_id: int
