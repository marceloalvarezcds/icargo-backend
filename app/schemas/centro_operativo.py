from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .centro_operativo_clasificacion import CentroOperativoClasificacion
from .centro_operativo_contacto_gestor_carga import (
    CentroOperativoContactoGestorCargaList,
)
from .ciudad import Ciudad
from .contacto import ContactoForm
from .gestor_carga_centro_operativo import GestorCargaCentroOperativo


class CentroOperativoBaseModel(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    clasificacion_id: int
    telefono: Optional[str] = None
    email: Optional[str] = None
    pagina_web: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None
    estado: Optional[str] = None


class CentroOperativoForm(CentroOperativoBaseModel):
    alias: Optional[str] = None
    contactos: List[ContactoForm]


class CentroOperativoBase(CentroOperativoBaseModel):
    id: int
    logo: Optional[str] = None
    estado: EstadoEnum
    clasificacion: CentroOperativoClasificacion
    ciudad: Optional[Ciudad] = None


class CentroOperativoList(CentroOperativoBase):
    clasificacion_nombre: Optional[str] = None
    ciudad_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    created_by: str #Agregar para vista CO

    class Config:
        orm_mode = True
        use_enum_values = True


class CentroOperativo(CentroOperativoBase):
    contactos: List[CentroOperativoContactoGestorCargaList] = []
    gestor_carga_centro_operativo: Optional[GestorCargaCentroOperativo] = None

    class Config:
        orm_mode = True
        use_enum_values = True
