from pydantic import BaseModel

from .date_model import Date
from .estado_base_model import EstadoBaseModel


class SeleccionableFormBaseModel(BaseModel):
    descripcion: str


class SeleccionableBaseModel(EstadoBaseModel):
    id: int
    descripcion: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
