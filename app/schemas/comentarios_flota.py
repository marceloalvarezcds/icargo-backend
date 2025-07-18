from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ComentarioFlotaForm(BaseModel):
    comentable_type: str
    comentable_id: int
    comentario: str
    tipo_evento: Optional[str]
    archivo: Optional[str]


class ComentarioFlota(ComentarioFlotaForm):
    id: int
    comentable_type: str
    comentable_id: int
    comentario: str
    tipo_evento: Optional[str]
    archivo: Optional[str]

    created_by: str
    created_at: datetime
    modified_by: str

    class Config:
        orm_mode = True
        use_enum_values = True


class ComentarioFlotaList(BaseModel):
    id: int
    comentable_type: str
    comentable_id: int
    comentario: str
    archivo: Optional[str]
    tipo_evento: Optional[str]
    created_by: Optional [str] = None
    created_at: datetime
    modified_by: str

    class Config:
        orm_mode = True
        use_enum_values = True
