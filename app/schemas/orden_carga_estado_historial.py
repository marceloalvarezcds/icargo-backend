from typing import Union

from pydantic import BaseModel

from app.enums import EstadoEnum, OrdenCargaEstadoEnum

from .date_model import Date


class OrdenCargaEstadoHistorial(BaseModel):
    id: int
    orden_carga_id: int
    estado: Union[EstadoEnum, OrdenCargaEstadoEnum]
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
