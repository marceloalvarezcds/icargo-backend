from pydantic import BaseModel

from .pais import Pais


class Localidad(BaseModel):
    id: int
    nombre: str
    pais_id: int
    pais: Pais

    class Config:
        orm_mode = True
