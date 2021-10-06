from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .centro_operativo_clasificacion import CentroOperativoClasificacion
from .ciudad import Ciudad
from .contacto import Contacto


class CentroOperativo(BaseModel):
    id: int
    nombre: str
    nombre_corto: Optional[str] = None
    logo: Optional[str] = None
    es_moderado: bool
    direccion: Optional[str] = None
    latitud: Decimal
    longitud: Decimal
    clasificacion_id: int
    clasificacion: CentroOperativoClasificacion
    ciudad_id: int
    ciudad: Ciudad
    contacto_id: Optional[int] = None
    contacto: Optional[Contacto] = None

    class Config:
        orm_mode = True


class CentroOperativoList(CentroOperativo):
    clasificacion_nombre: str
    ciudad_nombre: str
    localidad_nombre: str
    pais_nombre: str
    pais_nombre_corto: str
