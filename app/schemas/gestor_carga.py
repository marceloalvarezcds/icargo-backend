from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .ciudad import Ciudad
from .composicion_juridica import ComposicionJuridica
from .moneda import Moneda
from .tipo_documento import TipoDocumento


class GestorCargaForm(BaseModel):
    nombre: str
    nombre_corto: Optional[str] = None
    tipo_documento_id: int
    numero_documento: str
    digito_verificador: Optional[str] = None
    composicion_juridica_id: Optional[int] = None
    moneda_id: int
    telefono: Optional[str] = None
    email: Optional[str] = None
    pagina_web: Optional[str] = None
    info_complementaria: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    ciudad_id: Optional[int] = None
    # INICIO Limitaciones de la Gestora
    limite_cantidad_oc_activas: int
    # FIN Limitaciones de la Gestora
    estado: Optional[str] = None


class GestorCarga(GestorCargaForm):
    id: int
    tipo_documento: TipoDocumento
    composicion_juridica: Optional[ComposicionJuridica] = None
    moneda: Moneda
    logo: Optional[str] = None
    estado: EstadoEnum
    ciudad: Optional[Ciudad] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class GestorCargaList(GestorCarga):
    ciudad_nombre: Optional[str] = None
    composicion_juridica_nombre: Optional[str] = None
    localidad_nombre: Optional[str] = None
    moneda_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    tipo_documento_descripcion: Optional[str] = None
    created_by: str #Agregar para vista GC
