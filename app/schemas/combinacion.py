from datetime import datetime
from typing import Optional


from pydantic import BaseModel

from .camion import Camion
from .semi import Semi
from .propietario import Propietario
from .chofer import Chofer
from .camion_semi_neto import CamionSemiNeto
from app.enums import EstadoEnum
from .rounded_decimal_model import RoundedDecimal

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
    composicion_juridica_id: Optional[int] = None
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
    neto: RoundedDecimal
    class Config:
        orm_mode = True
        use_enum_values = True


class CombinacionForm(CombinacionBaseModel):
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
    oc_activa: Optional[int]
    limite_anticipos: Optional[int]
    puede_recibir_anticipos: bool
    anticipo_propietario: bool


class Combinaciones(CombinacionGet):
    propietario_nombre: Optional[str] = None
    propietario_ruc: Optional[str] = None
    chofer_nombre: str
    producto_descripcion: Optional[str] = None
    camion_propietario_nombre: Optional[str] = None
    camion_propietario_documento: Optional[str] = None
    semi_placa: str
    marca_descripcion: Optional[str] = None
    camion_placa: str
    marca_descripcion_semi: Optional[str] = None
    foto_camion: Optional[str] = None
    color_camion: Optional[str] = None
    chofer_numero_documento: Optional[str] = None
    puede_recibir_anticipos: bool
    anticipo_propietario: bool
    composicion_juridica_id: Optional[int] = None
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
    is_chofer_condicionado: bool
    is_propietario_condicionado: bool
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

class CombinacionUpdate(BaseModel):
    camion_id: Optional[int]
    semi_id: Optional[int]
    chofer_id: Optional[int]
    propietario_id: Optional[int]
    composicion_juridica_id: Optional[int] = None
    puede_recibir_anticipos: bool
    camion_oc_activa: Optional[int] = None
    limite_monto_anticipos: Optional[RoundedDecimal] = None

