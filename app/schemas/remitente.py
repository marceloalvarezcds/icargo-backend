from typing import List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .composicion_juridica import ComposicionJuridica
from .contacto import ContactoForm
from .gestor_carga_remitente import GestorCargaRemitente
from .remitente_contacto_gestor_carga import RemitenteContactoGestorCargaList
from .rounded_decimal_model import RoundedDecimal
from .tipo_documento import TipoDocumento


class RemitenteBaseModel(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    tipo_documento_id: int
    numero_documento: str
    digito_verificador: Optional[str] = None
    composicion_juridica_id: Optional[int] = None
    telefono: str
    email: Optional[str] = None
    pagina_web: Optional[str] = None
    info_complementaria: Optional[str] = None
    latitud: Optional[RoundedDecimal] = None
    longitud: Optional[RoundedDecimal] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None


class RemitenteForm(RemitenteBaseModel):
    alias: Optional[str] = None
    contactos: List[ContactoForm]


class RemitenteBase(RemitenteBaseModel):
    id: int
    tipo_documento: TipoDocumento
    composicion_juridica: Optional[ComposicionJuridica] = None
    logo: Optional[str] = None
    estado: EstadoEnum
    ciudad: Optional[Ciudad] = None


class RemitenteList(RemitenteBase):
    ciudad_nombre: Optional[str] = None
    composicion_juridica_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    tipo_documento_descripcion: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class Remitente(RemitenteBase):
    contactos: List[RemitenteContactoGestorCargaList] = []
    gestor_carga_remitente: Optional[GestorCargaRemitente] = None

    class Config:
        orm_mode = True
        use_enum_values = True
