from datetime import datetime
from typing import Optional

from .chofer import Chofer
from. propietario import Propietario
from .camion import Camion
from .semi import Semi
from pydantic import BaseModel
from app.enums import EstadoEnum


class CombinacionBaseModel(BaseModel):
    # id: int
    # estado: EstadoEnum
    propietario_id: int
    camion_id: int
    chofer_id: int
    semi_id: int
    comentario: str
    capacidad_total_combinacion: int

    class Config:
        orm_mode = True
        use_enum_values = True

class CombinacionForm(CombinacionBaseModel):
    camion: Optional[Camion]
    semi: Optional[Semi]
    propietario: Optional[Propietario]
    chofer: Optional[Chofer]
        

class CombinacionEditForm(BaseModel):
    propietario_id: int
    camion_id: int
    chofer_id: int
    semi_id: int
    comentario: str
    capacidad_total_combinacion: int
    camion: Optional[Camion]
    semi: Optional[Semi]
    propietario: Optional[Propietario]
    chofer: Optional[Chofer]
        

class CombinacionBase(BaseModel):
    id: int
    estado: str
    propietario_id: int
    camion_id: int
    chofer_id: int
    semi_id: int
    comentario: str
    capacidad_total_combinacion: int
    estado: EstadoEnum
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True

class CombinacionCreateModel(CombinacionBaseModel):
    pass

class CombinacionInDB(CombinacionBaseModel):
    id: int

    class Config:
        orm_mode = True


class Combinacion(CombinacionBase):
    camion: Optional[Camion]
    semi: Optional[Semi]
    propietario: Optional[Propietario]
    chofer: Optional[Chofer]

class CombinacionList(CombinacionBase):
    pass
 
