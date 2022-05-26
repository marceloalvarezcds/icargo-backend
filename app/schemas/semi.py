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
    ciudad_habilitacion_municipal_id: int
    numero_habilitacion_municipal: str
    vencimiento_habilitacion_municipal: Date
    foto_habilitacion_municipal_frente: Optional[str] = None
    foto_habilitacion_municipal_reverso: Optional[str] = None
    # fin - municipal
    # inicio - transporte
    ente_emisor_transporte_id: int
    numero_habilitacion_transporte: str
    vencimiento_habilitacion_transporte: Date
    foto_habilitacion_transporte_frente: Optional[str] = None
    foto_habilitacion_transporte_reverso: Optional[str] = None
    # fin - transporte
    # inicio - automotor
    ente_emisor_automotor_id: int
    titular_habilitacion_automotor: Optional[str] = None
    foto_habilitacion_automotor_frente: Optional[str] = None
    foto_habilitacion_automotor_reverso: Optional[str] = None
    # fin - automotor
    # FIN Habilitaciones del Camión
    # INICIO Detalles del Camión
    marca_id: int
    clasificacion_id: int
    tipo_id: int
    tipo_carga_id: int
    color_id: Optional[int] = None
    anho: int
    # FIN Detalles del Camión
    # INICIO Capacidad del Camión
    bruto: RoundedDecimal
    tara: RoundedDecimal
    largo: RoundedDecimal
    alto: RoundedDecimal
    ancho: RoundedDecimal
    volumen: RoundedDecimal
    # FIN Capacidad del Camión


class Semi(SemiForm):
    id: int
    propietario: Propietario
    estado: EstadoEnum
    gestor_cuenta_id: int
    info: str
    # INICIO Habilitaciones del Camión
    # inicio - municipal
    ciudad_habilitacion_municipal: Ciudad
    # fin - municipal
    # inicio - transporte
    ente_emisor_transporte: EnteEmisorTransporte
    # fin - transporte
    # inicio - automotor
    ente_emisor_automotor: EnteEmisorAutomotor
    pais_emisor_placa_nombre: str
    pais_emisor_placa_nombre_corto: str
    # fin - automotor
    # FIN Habilitaciones del Camión
    # INICIO Detalles del Camión
    marca: MarcaSemi
    clasificacion: SemiClasificacion
    tipo: TipoSemi
    tipo_carga: TipoCarga
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
    ciudad_habilitacion_municipal_nombre: str
    clasificacion_descripcion: str
    gestor_cuenta_id: int
    gestor_cuenta_nombre: str
    localidad_habilitacion_municipal_nombre: str
    info: str
    marca_descripcion: str
    oficial_cuenta_nombre: str
    pais_habilitacion_municipal_nombre: str
    pais_habilitacion_municipal_nombre_corto: str
    pais_emisor_placa_nombre: str
    pais_emisor_placa_nombre_corto: str
    tipo_descripcion: str
    tipo_carga_descripcion: str
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
