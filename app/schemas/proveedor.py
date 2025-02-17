from decimal import Decimal
from typing import Any, List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .composicion_juridica import ComposicionJuridica
from .contacto import ContactoForm
from .gestor_carga_proveedor import GestorCargaProveedor
from .proveedor_contacto_gestor_carga import ProveedorContactoGestorCargaList
from .tipo_documento import TipoDocumento


class ProveedorBaseModel(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    tipo_documento_id: int
    numero_documento: str
    digito_verificador: Optional[str] = None
    composicion_juridica_id: Optional[int] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    pagina_web: Optional[str] = None
    info_complementaria: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None
    estado: Optional[str] = None


class ProveedorForm(ProveedorBaseModel):
    alias: Optional[str] = None
    contactos: List[ContactoForm]
    created_at: str


class ProveedorBase(ProveedorBaseModel):
    id: int
    tipo_documento: TipoDocumento
    composicion_juridica: Optional[ComposicionJuridica] = None
    logo: Optional[str] = None
    estado: EstadoEnum
    ciudad: Optional[Ciudad] = None


class ProveedorList(ProveedorBase):
    ciudad_nombre: Optional[str] = None
    composicion_juridica_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    tipo_documento_descripcion: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class Proveedor(ProveedorBase):
    contactos: List[ProveedorContactoGestorCargaList] = []
    gestor_carga_proveedor: Optional[GestorCargaProveedor] = None

    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def from_orm(cls, obj: Any) -> "Proveedor":
        obj.contactos = []
        obj.gestor_carga_proveedor = None
        return super().from_orm(obj)
