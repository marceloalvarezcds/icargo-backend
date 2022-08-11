from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .date_model import Date
from .gestor_carga_chofer import GestorCargaChofer
from .localidad import Localidad
from .pais import Pais
from .tipo_documento import TipoDocumento
from .tipo_registro import TipoRegistro


class ChoferBaseModel(BaseModel):
    nombre: str
    tipo_documento_id: int
    pais_emisor_documento_id: int
    numero_documento: str
    ruc: Optional[str] = None
    digito_verificador: Optional[str] = None
    fecha_nacimiento: Optional[Date] = None
    oficial_cuenta_id: Optional[int] = None
    foto_documento_frente: Optional[str] = None
    foto_documento_reverso: Optional[str] = None
    foto_perfil: Optional[str] = None
    es_propietario: Optional[bool] = False
    puede_recibir_anticipos: bool
    # Datos del Propietario
    pais_origen_id: Optional[int] = None
    foto_documento_frente_propietario: Optional[str] = None
    foto_documento_reverso_propietario: Optional[str] = None
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
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[str] = None


class ChoferForm(ChoferBaseModel):
    alias: Optional[str] = None


class ChoferEditForm(BaseModel):
    nombre: Optional[str] = None
    tipo_documento_id: Optional[int] = None
    pais_emisor_documento_id: Optional[int] = None
    numero_documento: Optional[str] = None
    ruc: Optional[str] = None
    digito_verificador: Optional[str] = None
    fecha_nacimiento: Optional[Date] = None
    oficial_cuenta_id: Optional[int] = None
    foto_documento_frente: Optional[str] = None
    foto_documento_reverso: Optional[str] = None
    foto_perfil: Optional[str] = None
    es_propietario: Optional[bool] = False
    puede_recibir_anticipos: bool
    anticipos_bloqueados: Optional[bool] = False
    # Datos del Propietario
    pais_origen_id: Optional[int] = None
    foto_documento_frente_propietario: Optional[str] = None
    foto_documento_reverso_propietario: Optional[str] = None
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
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None
    alias: Optional[str] = None


class ChoferBase(ChoferBaseModel):
    id: int
    tipo_documento: TipoDocumento
    pais_emisor_documento: Pais
    gestor_cuenta_id: int
    gestor_cuenta_nombre: str
    oficial_cuenta_nombre: Optional[str] = None
    # Datos del Propietario
    pais_origen: Optional[Pais] = None
    # inicio registro
    pais_emisor_registro: Optional[Pais] = None
    localidad_emisor_registro: Optional[Localidad] = None
    ciudad_emisor_registro: Optional[Ciudad] = None
    tipo_registro: Optional[TipoRegistro] = None
    # fin registro
    estado: EstadoEnum
    ciudad: Optional[Ciudad] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class ChoferList(BaseModel):
    id: int
    nombre: str
    tipo_documento_id: int
    tipo_documento_descripcion: Optional[str] = None
    pais_emisor_documento_id: int
    pais_emisor_documento_nombre: Optional[str] = None
    pais_emisor_documento_nombre_corto: Optional[str] = None
    numero_documento: str
    fecha_nacimiento: Optional[Date] = None
    gestor_cuenta_id: int
    gestor_cuenta_nombre: str
    oficial_cuenta_nombre: Optional[str] = None
    es_propietario: Optional[bool] = False
    estado: EstadoEnum
    direccion: Optional[str] = None
    ciudad: Optional[Ciudad] = None
    ciudad_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class Chofer(ChoferBase):
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime
    gestor_carga_chofer: Optional[GestorCargaChofer] = None
    oc_with_anticipos_liberados: Optional[int] = None

    @classmethod
    def from_orm(cls, obj: Any) -> "Chofer":
        obj.gestor_carga_chofer = None
        obj.foto_documento_frente_propietario = None
        obj.foto_documento_reverso_propietario = None
        obj.pais_origen_id = None
        obj.pais_origen = None
        obj.oc_with_anticipos_liberados = None
        return super().from_orm(obj)
