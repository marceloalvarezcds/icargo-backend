from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .contacto import ContactoForm
from .date_model import Date
from .gestor_carga_propietario import GestorCargaPropietario
from .pais import Pais
from .propietario_contacto_gestor_carga import PropietarioContactoGestorCargaList
from .tipo_persona import TipoPersona


class PropietarioBaseModel(BaseModel):
    nombre: str
    tipo_persona_id: int
    ruc: str
    digito_verificador: str
    pais_origen_id: int
    fecha_nacimiento: Optional[Date] = None
    oficial_cuenta_id: int
    foto_documento_frente: Optional[str] = None
    foto_documento_reverso: Optional[str] = None
    foto_perfil: Optional[str] = None
    es_chofer: bool = False
    telefono: str
    email: Optional[str] = None
    direccion: Optional[str] = None
    ciudad_id: int


class PropietarioForm(PropietarioBaseModel):
    pais_id: int
    localidad_id: int
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
    pais_origen: Pais
    gestor_cuenta_id: int
    gestor_cuenta_nombre: str
    oficial_cuenta_nombre: Optional[str] = None
    estado: EstadoEnum
    ciudad: Ciudad

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
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime
    contactos: List[PropietarioContactoGestorCargaList] = []
    gestor_carga_propietario: Optional[GestorCargaPropietario] = None
