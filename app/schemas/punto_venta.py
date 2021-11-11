from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .composicion_juridica import ComposicionJuridica
from .contacto import ContactoForm
from .gestor_carga_punto_venta import GestorCargaPuntoVenta
from .punto_venta_contacto_gestor_carga import PuntoVentaContactoGestorCargaList
from .tipo_documento import TipoDocumento


class PuntoVentaBaseModel(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    proveedor_id: int
    tipo_documento_id: int
    numero_documento: str
    digito_verificador: Optional[str] = None
    composicion_juridica_id: int
    telefono: str
    email: Optional[str] = None
    pagina_web: Optional[str] = None
    info_complementaria: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None


class PuntoVentaForm(PuntoVentaBaseModel):
    alias: Optional[str] = None
    contactos: List[ContactoForm]


class PuntoVentaBase(PuntoVentaBaseModel):
    id: int
    tipo_documento: TipoDocumento
    composicion_juridica: ComposicionJuridica
    logo: Optional[str] = None
    estado: EstadoEnum
    ciudad: Optional[Ciudad] = None


class PuntoVentaList(PuntoVentaBase):
    ciudad_nombre: Optional[str] = None
    composicion_juridica_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    tipo_documento_descripcion: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class PuntoVenta(PuntoVentaBase):
    contactos: List[PuntoVentaContactoGestorCargaList] = []
    gestor_carga_punto_venta: Optional[GestorCargaPuntoVenta] = None
