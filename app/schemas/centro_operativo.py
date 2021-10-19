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


class CentroOperativoBaseModel(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    clasificacion_id: int
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None


class CentroOperativoForm(CentroOperativoBaseModel):
    alias: str
    contactos: List[ContactoForm]


class CentroOperativo(CentroOperativoBaseModel):
    id: int
    logo: Optional[str] = None
    estado: EstadoEnum
    clasificacion: CentroOperativoClasificacion
    ciudad: Optional[Ciudad] = None
    contactos: List[CentroOperativoContactoGestorCargaList]

    class Config:
        orm_mode = True
        use_enum_values = True


class CentroOperativoList(CentroOperativo):
    clasificacion_nombre: Optional[str] = None
    ciudad_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
