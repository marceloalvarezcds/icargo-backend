from typing import Optional

from .estado_base_model import EstadoBaseModel
from datetime import datetime

class InsumoForm(EstadoBaseModel):
    descripcion: str
    tipo_id: int
    unidad_id: Optional[int]


class Insumo(InsumoForm):
    id: int
    tipo_descripcion: str
    unidad_descripcion: Optional[str]
    unidad_abreviatura: Optional[str]
    fecha_creacion: Optional[datetime] = None

    class Config:
        orm_mode = True
