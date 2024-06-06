from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .color import Color
from .date_model import Date
from .ente_emisor_automotor import EnteEmisorAutomotor
from .ente_emisor_transporte import EnteEmisorTransporte
from .marca_semi import MarcaSemi
from .propietario import Propietario
from .rounded_decimal_model import RoundedDecimal
from .semi_clasificacion import SemiClasificacion
from .tipo_carga import TipoCarga
from .tipo_semi import TipoSemi


class SemiForm(BaseModel):
    placa: str
    propietario_id: int
    numero_chasis: Optional[str] = None
    foto: Optional[str] = None
    # INICIO Habilitaciones del Camión
    # inicio - municipal
    pais_habilitacion_municipal_id: Optional[int] = None
    localidad_habilitacion_municipal_id: Optional[int] = None
    ciudad_habilitacion_municipal_id: Optional[int] = None
    numero_habilitacion_municipal: Optional[str] = None
    vencimiento_habilitacion_municipal: Optional[Date] = None
    foto_habilitacion_municipal_frente: Optional[str] = None
    foto_habilitacion_municipal_reverso: Optional[str] = None
    # fin - municipal
    # inicio - transporte
    ente_emisor_transporte_id: Optional[int] = None
    numero_habilitacion_transporte: Optional[str] = None
    vencimiento_habilitacion_transporte: Optional[Date] = None
    foto_habilitacion_transporte_frente: Optional[str] = None
    foto_habilitacion_transporte_reverso: Optional[str] = None
    # fin - transporte
    # inicio - automotor
    ente_emisor_automotor_id: Optional[int] = None
    titular_habilitacion_automotor: Optional[str] = None
    foto_habilitacion_automotor_frente: Optional[str] = None
    foto_habilitacion_automotor_reverso: Optional[str] = None
    # fin - automotor
    # FIN Habilitaciones del Camión
    # INICIO Detalles del Camión
    marca_id: Optional[int] = None
    clasificacion_id: Optional[int] = None
    tipo_id: Optional[int] = None
    tipo_carga_id: Optional[int] = None
    color_id: Optional[int] = None
    anho: Optional[int] = None
    # FIN Detalles del Camión
    # INICIO Capacidad del Camión
    bruto: Optional[RoundedDecimal] = None
    tara: Optional[RoundedDecimal] = None
    largo: Optional[RoundedDecimal] = None
    alto: Optional[RoundedDecimal] = None
    ancho: Optional[RoundedDecimal] = None
    volumen: Optional[RoundedDecimal] = None
    # FIN Capacidad del Camión


class Semi(SemiForm):
    id: int
    propietario: Propietario
    estado: EstadoEnum
    gestor_cuenta_id: int
    info: str
    # INICIO Habilitaciones del Camión
    # inicio - municipal
    ciudad_habilitacion_municipal: Optional[Ciudad] = None
    localidad_habilitacion_municipal_id: Optional[int] = None
    localidad_habilitacion_municipal_nombre: Optional[str] = None
    pais_habilitacion_municipal_id: Optional[int] = None
    pais_habilitacion_municipal_nombre: Optional[str] = None
    pais_habilitacion_municipal_nombre_corto: Optional[str] = None
    # fin - municipal
    # inicio - transporte
    ente_emisor_transporte: Optional[EnteEmisorTransporte] = None
    # fin - transporte
    # inicio - automotor
    ente_emisor_automotor: Optional[EnteEmisorAutomotor] = None
    pais_emisor_placa_nombre: Optional[str] = None
    pais_emisor_placa_nombre_corto: Optional[str] = None
    # fin - automotor
    # FIN Habilitaciones del Camión
    # INICIO Detalles del Camión
    marca: Optional[MarcaSemi] = None
    clasificacion: Optional[SemiClasificacion] = None
    tipo: Optional[TipoSemi] = None
    tipo_carga: Optional[TipoCarga] = None
    color: Optional[Color] = None
    # FIN Detalles del Camión
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class SemiList(BaseModel):
    id: int
    placa: str
    propietario_nombre: str
    propietario_ruc: str
    numero_chasis: Optional[str] = None
    estado: EstadoEnum
    ciudad_habilitacion_municipal_nombre: Optional[str] = None
    clasificacion_descripcion: Optional[str] = None
    gestor_cuenta_id: int
    gestor_cuenta_nombre: Optional[str] = None
    localidad_habilitacion_municipal_id: Optional[int] = None
    localidad_habilitacion_municipal_nombre: Optional[str] = None
    info: str
    color_descripcion: Optional[str] = None
    foto:  Optional[str] = None
    marca_descripcion: Optional[str] = None
    oficial_cuenta_nombre: Optional[str] = None
    pais_habilitacion_municipal_id: Optional[int] = None
    pais_habilitacion_municipal_nombre: Optional[str] = None
    pais_habilitacion_municipal_nombre_corto: Optional[str] = None
    pais_emisor_placa_nombre: Optional[str] = None
    pais_emisor_placa_nombre_corto: Optional[str] = None
    tipo_descripcion: Optional[str] = None
    tipo_carga_descripcion: Optional[str] = None
    created_by: Optional [str] = None
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True

# class SemiCominacion(BaseModel):
#     placa: str
#     estado: EstadoEnum
#     class Config:
#         orm_mode = True
#         use_enum_values = True