from datetime import datetime
from typing import Optional


from pydantic import BaseModel

from .camion import Camion
from .semi import Semi
from .propietario import Propietario
from .chofer import Chofer
from .camion_semi_neto import CamionSemiNeto
from app.enums import EstadoEnum


class CombinacionGet(BaseModel):
    id: int
    estado: EstadoEnum
    propietario_id: int
    camion_id: int
    chofer_id: int
    semi_id: int
    camion: Camion
    semi: Semi
    propietario: Propietario
    chofer: Chofer
    neto: int
    comentario: Optional[str] = None
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class CombinacionBaseModel(BaseModel):
    propietario_id: int
    camion_id: int
    chofer_id: int
    semi_id: int
    gestor_carga_id: Optional[int]
   
    comentario: Optional[str]
    neto: int

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
    gestor_carga_id: int
    camion: Optional[Camion]
    semi: Optional[Semi]
    propietario: Optional[Propietario]
    chofer: Optional[Chofer]


class CombinacionBase(BaseModel):
    propietario_id: int
    camion_id: int
    chofer_id: int
    semi_id: int

    class Config:
        orm_mode = True
        use_enum_values = True


class CombinacionCreateModel(CombinacionBaseModel):
    pass


class Combinaciones(CombinacionGet):
    propietario_nombre: Optional[str] = None
    chofer_nombre: str
    producto_descripcion: Optional[str] = None
    semi_placa: str
    marca_descripcion: Optional[str] = None
    camion_placa: str
    marca_descripcion_semi: Optional[str] = None
    foto_camion: Optional[str] = None
    class Config:
        orm_mode = True


class CombinacionesBD(Combinaciones):
    pass


class Combinacion(CombinacionBase):
    camion: Optional[Camion]
    semi: Optional[Semi]
    propietario: Optional[Propietario]
    chofer: Optional[Chofer]


class CombinacionList(CombinacionBase):
    camion: Camion
    semi: Semi
    propietario: Propietario
    chofer: Chofer
    camion_semi_neto: Optional[CamionSemiNeto] = None
    comentario: str
    
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True


class CombinacionWithJoin(CombinacionBase):
    camion: Camion
    semi: Semi
    propietario: Propietario
    chofer: Chofer
    camion_semi_neto: Optional[CamionSemiNeto] = None

    class Config:
        orm_mode = True
