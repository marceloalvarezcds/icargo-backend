from pydantic import BaseModel

from .localidad import Localidad


class Ciudad(BaseModel):
    id: int
    nombre: str
    localidad_id: int
    localidad: Localidad

    class Config:
        orm_mode = True
