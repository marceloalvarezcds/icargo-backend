from typing import Union

from pydantic import BaseModel

from app.enums import EstadoEnum, OrdenCargaEstadoEnum

from .date_model import Date

from typing import Optional

class OrdenCargaComentariosHistorial(BaseModel):
    id: Optional[int]
    orden_carga_id: Optional[int]
    comentario: Optional[str] = None  # Asegúrate de que puede ser None
    created_by: Optional[str] = None
    created_at: Optional[Date] = None
    modified_by: Optional[str] = None
    modified_at: Optional[Date] = None

    class Config:
        orm_mode = True
