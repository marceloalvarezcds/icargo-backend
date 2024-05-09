from datetime import datetime
from typing import Optional

from .producto import Producto
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
    producto_id: int
    gestor_carga_id: int
    neto: int
    comentario: str
    capacidad_total_combinacion: int
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
    camion_semi_neto: Optional[CamionSemiNeto] = None


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
    camion: Camion
    semi: Semi
    propietario: Propietario
    chofer: Chofer
    producto: Producto

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
    capacidad_total_combinacion: int
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
