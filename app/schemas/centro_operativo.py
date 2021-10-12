from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .centro_operativo_clasificacion import CentroOperativoClasificacion
from .ciudad import Ciudad
from .contacto import Contacto


class CentroOperativoBaseModel(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    clasificacion_id: int
    direccion: Optional[str] = None
    ciudad_id: int


class CentroOperativoForm(CentroOperativoBaseModel):
    alias: str


class CentroOperativo(CentroOperativoBaseModel):
    id: int
    logo: Optional[str] = None
    estado: EstadoEnum
    latitud: Decimal
    longitud: Decimal
    clasificacion: CentroOperativoClasificacion
    ciudad: Ciudad
    contactos: List[Contacto]

    class Config:
        orm_mode = True
        use_enum_values = True


class CentroOperativoList(CentroOperativo):
    clasificacion_nombre: str
    ciudad_nombre: str
    localidad_nombre: str
    pais_nombre: str
    pais_nombre_corto: str
