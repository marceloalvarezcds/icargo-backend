from typing import Optional

from .estado_base_model import EstadoBaseModel


class InsumoForm(EstadoBaseModel):
    descripcion: str
    tipo_id: int
    unidad_id: Optional[int]


class Insumo(InsumoForm):
    id: int
    tipo_descripcion: str
    unidad_descripcion: Optional[str]
    unidad_abreviatura: Optional[str]

    class Config:
        orm_mode = True
