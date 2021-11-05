from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum
from app.schemas.gestor_carga_centro_operativo import GestorCargaCentroOperativo

from .centro_operativo_clasificacion import CentroOperativoClasificacion
from .centro_operativo_contacto_gestor_carga import (
    CentroOperativoContactoGestorCargaList,
)
from .ciudad import Ciudad
from .contacto import ContactoForm


class CentroOperativoBaseModel(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    clasificacion_id: int
    telefono: str
    email: Optional[str] = None
    pagina_web: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    ciudad_id: int


class CentroOperativoForm(CentroOperativoBaseModel):
    alias: Optional[str] = None
    contactos: List[ContactoForm]


class CentroOperativoBase(CentroOperativoBaseModel):
    id: int
    logo: Optional[str] = None
    estado: EstadoEnum
    clasificacion: CentroOperativoClasificacion
    ciudad: Ciudad


class CentroOperativoList(CentroOperativoBase):
    clasificacion_nombre: Optional[str] = None
    ciudad_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class CentroOperativo(CentroOperativoBase):
    contactos: List[CentroOperativoContactoGestorCargaList] = []
    gestor_carga_centro_operativo: Optional[GestorCargaCentroOperativo] = None
