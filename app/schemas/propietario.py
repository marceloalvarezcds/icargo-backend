from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .contacto import ContactoForm
from .date_model import Date
from .gestor_carga_propietario import GestorCargaPropietario
from .localidad import Localidad
from .pais import Pais
from .propietario_contacto_gestor_carga import PropietarioContactoGestorCargaList
from .tipo_documento import TipoDocumento
from .tipo_persona import TipoPersona
from .tipo_registro import TipoRegistro


class PropietarioBaseModel(BaseModel):
    nombre: str
    tipo_persona_id: int
    ruc: str
    digito_verificador: Optional[str] = None
    pais_origen_id: Optional[int] = None
    fecha_nacimiento: Optional[Date] = None
    oficial_cuenta_id: Optional[int] = None
    foto_documento_frente: Optional[str] = None
    foto_documento_reverso: Optional[str] = None
    foto_perfil: Optional[str] = None
    es_chofer: Optional[bool] = False
    puede_recibir_anticipos: bool
    # INICIO Datos del Chofer
    tipo_documento_id: Optional[int] = None
    pais_emisor_documento_id: Optional[int] = None
    numero_documento: Optional[str] = None
    foto_documento_frente_chofer: Optional[str] = None
    foto_documento_reverso_chofer: Optional[str] = None
    # inicio registro
    pais_emisor_registro_id: Optional[int] = None
    localidad_emisor_registro_id: Optional[int] = None
    ciudad_emisor_registro_id: Optional[int] = None
    tipo_registro_id: Optional[int] = None
    numero_registro: Optional[str] = None
    vencimiento_registro: Optional[Date] = None
    foto_registro_frente: Optional[str] = None
    foto_registro_reverso: Optional[str] = None
    # fin registro
    # FIN Datos del Chofer
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None


class PropietarioForm(PropietarioBaseModel):
    pais_id: Optional[int] = None
    localidad_id: Optional[int] = None
    alias: Optional[str] = None
    contactos: List[ContactoForm]


class PropietarioEditForm(BaseModel):
    nombre: Optional[str] = None
    tipo_persona_id: Optional[int] = None
    ruc: Optional[str] = None
    digito_verificador: Optional[str] = None
    pais_origen_id: Optional[int] = None
    fecha_nacimiento: Optional[Date] = None
    oficial_cuenta_id: Optional[int] = None
    foto_documento_frente: Optional[str] = None
    foto_documento_reverso: Optional[str] = None
    foto_perfil: Optional[str] = None
    es_chofer: Optional[bool] = False
    puede_recibir_anticipos: bool
    # INICIO Datos del Chofer
    tipo_documento_id: Optional[int] = None
    pais_emisor_documento_id: Optional[int] = None
    numero_documento: Optional[str] = None
    foto_documento_frente_chofer: Optional[str] = None
    foto_documento_reverso_chofer: Optional[str] = None
    # inicio registro
    pais_emisor_registro_id: Optional[int] = None
    localidad_emisor_registro_id: Optional[int] = None
    ciudad_emisor_registro_id: Optional[int] = None
    tipo_registro_id: Optional[int] = None
    numero_registro: Optional[str] = None
    vencimiento_registro: Optional[Date] = None
    foto_registro_frente: Optional[str] = None
    foto_registro_reverso: Optional[str] = None
    # fin registro
    # FIN Datos del Chofer
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None
    pais_id: Optional[int] = None
    localidad_id: Optional[int] = None
    alias: Optional[str] = None
    contactos: List[ContactoForm]


class PropietarioBase(PropietarioBaseModel):
    id: int
    tipo_persona: TipoPersona
    pais_origen: Optional[Pais] = None
    gestor_cuenta_id: int
    gestor_cuenta_nombre: str
    oficial_cuenta_nombre: Optional[str] = None
    # INICIO Datos del Chofer
    tipo_documento: Optional[TipoDocumento] = None
    pais_emisor_documento: Optional[Pais] = None
    # inicio registro
    pais_emisor_registro: Optional[Pais] = None
    localidad_emisor_registro: Optional[Localidad] = None
    ciudad_emisor_registro: Optional[Ciudad] = None
    tipo_registro: Optional[TipoRegistro] = None
    # fin registro
    # FIN Datos del Chofer
    estado: EstadoEnum
    ciudad: Optional[Ciudad] = None
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class PropietarioList(PropietarioBase):
    ciudad_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    pais_origen_nombre: Optional[str] = None
    pais_origen_nombre_corto: Optional[str] = None
    tipo_persona_descripcion: Optional[str] = None


class Propietario(PropietarioBase):
    contactos: List[PropietarioContactoGestorCargaList] = []
    gestor_carga_propietario: Optional[GestorCargaPropietario] = None
