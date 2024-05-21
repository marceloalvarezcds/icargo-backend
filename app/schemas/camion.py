from datetime import datetime
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
from .rounded_decimal_model import RoundedDecimal
from .tipo_camion import TipoCamion


class CamionForm(BaseModel):
    placa: str
    propietario_id: int
    gestor_carga_id: Optional[int] = None
    chofer_id: Optional[int] = None
    numero_chasis: Optional[str] = None
    foto: Optional[str] = None
    # INICIO Limitaciones del Camión
    limite_cantidad_oc_activas: int
    limite_monto_anticipos: Optional[RoundedDecimal] = None
    monto_anticipo_disponible: Optional[RoundedDecimal] = None
    total_anticipos_retirados_en_estado_pendiente_o_en_proceso: Optional[
        RoundedDecimal
    ] = None
    # FIN Limitaciones del Camión
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
    tipo_id: Optional[int] = None
    color_id: Optional[int] = None
    anho: Optional[int] = None
    # FIN Detalles del Camión
    # INICIO Capacidad del Camión
    bruto: Optional[RoundedDecimal] = None
    tara: Optional[RoundedDecimal] = None
    # FIN Capacidad del Camión


class Camion(CamionForm):
    id: int
    propietario: Propietario
    propietario_estado: EstadoEnum
    chofer: Optional[Chofer]
    chofer_estado: Optional[EstadoEnum] = None
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
    marca: Optional[MarcaCamion] = None
    tipo: Optional[TipoCamion] = None
    color: Optional[Color] = None
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
    propietario_telefono: Optional[str] = None
    chofer_nombre: Optional[str] = None
    chofer_numero_documento: Optional[str] = None
    color_descripcion: Optional[str] = None
    numero_chasis: Optional[str] = None
    estado: EstadoEnum
    ciudad_habilitacion_municipal_nombre: Optional[str] = None
    gestor_cuenta_id: int
    gestor_cuenta_nombre: str
    localidad_habilitacion_municipal_id: Optional[int] = None
    localidad_habilitacion_municipal_nombre: Optional[str] = None
    info: str
    marca_descripcion: Optional[str] = None
    oficial_cuenta_nombre: Optional[str] = None
    pais_habilitacion_municipal_id: Optional[int] = None
    pais_habilitacion_municipal_nombre: Optional[str] = None
    pais_habilitacion_municipal_nombre_corto: Optional[str] = None
    pais_emisor_placa_nombre: Optional[str] = None
    pais_emisor_placa_nombre_corto: Optional[str] = None
    tipo_descripcion: Optional[str] = None
    limites: str
    limite_monto_anticipo: Optional[int] = None
    foto_camion: Optional[str] =  None
    oc_activa: int
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True

