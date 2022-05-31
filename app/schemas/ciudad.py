from pydantic import BaseModel

from .localidad import Localidad


class Ciudad(BaseModel):
    id: int
    nombre: str
    localidad_id: int
    localidad_nombre: str
    localidad: Localidad
    pais_id: int
    pais_nombre: str
    pais_nombre_corto: str

    class Config:
        orm_mode = True
