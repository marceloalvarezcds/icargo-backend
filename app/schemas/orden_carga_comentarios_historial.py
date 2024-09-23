from typing import Union

from pydantic import BaseModel

from app.enums import EstadoEnum, OrdenCargaEstadoEnum

from .date_model import Date

from typing import Optional

class OrdenCargaComentariosHistorial(BaseModel):
    id: Optional[int]
    orden_carga_id: Optional[int]
    comentario: Optional[str]
    # Auditoría
    created_by: Optional[str]
    created_at: Date
    modified_by: Optional[str]
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
