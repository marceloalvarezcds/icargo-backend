from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .chofer import Chofer
from .ciudad import Ciudad
from .color import Color
from .date_model import Date
from .ente_emisor_automotor import EnteEmisorAutomotor
from .ente_emisor_transporte import EnteEmisorTransporte
from .marca_camion import MarcaCamion
from .propietario import Propietario
from .tipo_camion import TipoCamion


class CamionForm(BaseModel):
    placa: str
    propietario_id: int
    chofer_id: Optional[int] = None
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
    tipo_id: int
    color_id: int
    anho: int
    # FIN Detalles del Camión
    # INICIO Capacidad del Camión
    bruto: Decimal
    tara: Decimal
    # FIN Capacidad del Camión


class Camion(CamionForm):
    id: int
    propietario: Propietario
    chofer: Optional[Chofer]
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
    marca: MarcaCamion
    tipo: TipoCamion
    color: Color
    # FIN Detalles del Camión
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class CamionList(BaseModel):
    id: int
    placa: str
    propietario_nombre: str
    propietario_ruc: str
    chofer_nombre: Optional[str] = None
    chofer_numero_documento: Optional[str] = None
    numero_chasis: Optional[str] = None
    estado: EstadoEnum
    ciudad_habilitacion_municipal_nombre: str
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
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
