from typing import Any, List, Optional

from pydantic import BaseModel

from app.enums import EstadoEnum, TipoFleteEnum

from .centro_operativo import CentroOperativo
from .date_model import Date
from .flete_anticipo import FleteAnticipo, FleteAnticipoForm
from .flete_complemento import FleteComplemento, FleteComplementoForm
from .flete_descuento import FleteDescuento, FleteDescuentoForm
from .flete_destinatario import FleteDestinatario
from .moneda import Moneda
from .producto import Producto
from .remitente import Remitente
from .rounded_decimal_model import RoundedDecimal
from .tipo_carga import TipoCarga
from .unidad import Unidad


class FleteFormBaseModel(BaseModel):
    remitente_id: int
    producto_id: int
    tipo_carga_id: Optional[int] = None
    numero_lote: Optional[str] = None
    publicado: Optional[bool] = False
    es_subasta: Optional[bool] = False
    # INICIO Tramo de Fletes
    origen_id: int
    origen_indicacion: Optional[str]
    destino_id: int
    destino_indicacion: Optional[str]
    distancia: Optional[RoundedDecimal]
    # FIN Tramo de Fletes
    # INICIO Cantidad y Flete
    condicion_cantidad: RoundedDecimal
    saldo: Optional[RoundedDecimal]
    # inicio - Condiciones para el Gestor de Carga
    condicion_gestor_carga_moneda_id: int
    condicion_gestor_carga_tarifa: RoundedDecimal
    condicion_gestor_carga_unidad_id: int
    # fin - Condiciones para el Gestor de Carga
    # inicio - Condiciones para el Propietario
    condicion_propietario_moneda_id: int
    condicion_propietario_tarifa: RoundedDecimal
    condicion_propietario_unidad_id: int
    # fin - Condiciones para el Propietario
    # FIN Cantidad y Flete
    # INICIO Mermas de Fletes
    # inicio - Mermas para el Gestor de Carga
    merma_gestor_carga_valor: RoundedDecimal
    merma_gestor_carga_moneda_id: int
    merma_gestor_carga_unidad_id: int
    merma_gestor_carga_es_porcentual: Optional[bool] = False
    merma_gestor_carga_tolerancia: RoundedDecimal
    # fin - Mermas para el Gestor de Carga
    # inicio - Mermas para el Propietario
    merma_propietario_valor: RoundedDecimal
    merma_propietario_moneda_id: int
    merma_propietario_unidad_id: int
    merma_propietario_es_porcentual: Optional[bool] = False
    merma_propietario_tolerancia: RoundedDecimal
    # fin - Mermas para el Propietario
    # FIN Mermas de Fletes
    vigencia_anticipos: Optional[Date] = None
    # INICIO Emisión de Órdenes
    emision_orden_texto_legal: Optional[str] = None
    emision_orden_detalle: Optional[str] = None
    # FIN Emisión de Órdenes


class FleteForm(FleteFormBaseModel):
    anticipos: List[FleteAnticipoForm]
    complementos: List[FleteComplementoForm]
    descuentos: List[FleteDescuentoForm]
    # INICIO Emisión de Órdenes
    destinatarios: Optional[List[FleteDestinatario]] = None
    # FIN Emisión de Órdenes


class Flete(FleteFormBaseModel):
    id: int
    remitente: Remitente
    producto: Producto
    tipo_carga: Optional[TipoCarga] = None
    publicado_descripcion: str
    estado: EstadoEnum
    gestor_carga_id: int
    # INICIO Tramo de Fletes
    origen: CentroOperativo
    destino: CentroOperativo
    # FIN Tramo de Fletes
    # INICIO Cantidad y Flete
    # inicio - Condiciones para el Gestor de Carga
    condicion_gestor_carga_moneda: Moneda
    condicion_gestor_carga_unidad: Unidad
    # fin - Condiciones para el Gestor de Carga
    # inicio - Condiciones para el Propietario
    condicion_propietario_moneda: Moneda
    condicion_propietario_unidad: Unidad
    # fin - Condiciones para el Propietario
    # FIN Cantidad y Flete
    # INICIO Mermas de Fletes
    # inicio - Mermas para el Gestor de Carga
    merma_gestor_carga_moneda: Moneda
    merma_gestor_carga_unidad: Unidad
    merma_gestor_carga_es_porcentual_descripcion: str
    # fin - Mermas para el Gestor de Carga
    # inicio - Mermas para el Propietario
    merma_propietario_moneda: Moneda
    merma_propietario_unidad: Unidad
    merma_propietario_es_porcentual_descripcion: str
    # fin - Mermas para el Propietario
    # FIN Mermas de Fletes
    # INICIO Emisión de Órdenes
    destinatarios: List[FleteDestinatario]
    # FIN Emisión de Órdenes
    anticipos: List[FleteAnticipo]
    complementos: List[FleteComplemento]
    descuentos: List[FleteDescuento]
    tipo_flete: Optional[TipoFleteEnum] = None
    is_in_orden_carga: bool
    info: str
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def from_orm(cls, obj: Any) -> "Flete":
        obj.destinatarios = []
        return super().from_orm(obj)


class FleteList(FleteFormBaseModel):
    id: int
    remitente_nombre: str
    producto_descripcion: str
    tipo_carga_descripcion: Optional[str] = None
    publicado_descripcion: str
    estado: EstadoEnum
    gestor_carga_nombre: str
    # INICIO Tramo de Fletes
    origen_nombre: str
    destino_nombre: str
    # FIN Tramo de Fletes
    # INICIO Cantidad y Flete
    # inicio - Condiciones para el Gestor de Carga
    condicion_gestor_carga_moneda_nombre: str
    condicion_gestor_carga_unidad_descripcion: str
    # fin - Condiciones para el Gestor de Carga
    # inicio - Condiciones para el Propietario
    condicion_propietario_moneda_nombre: str
    condicion_propietario_unidad_descripcion: str
    condicion_propietario_tarifa_unidad: str
    # fin - Condiciones para el Propietario
    # FIN Cantidad y Flete
    # INICIO Mermas de Fletes
    # inicio - Mermas para el Gestor de Carga
    merma_gestor_carga_moneda_nombre: str
    merma_gestor_carga_unidad_descripcion: str
    merma_gestor_carga_es_porcentual_descripcion: str
    # fin - Mermas para el Gestor de Carga
    # inicio - Mermas para el Propietario
    merma_propietario_moneda_nombre: str
    merma_propietario_unidad_descripcion: str
    merma_propietario_es_porcentual_descripcion: str
    # fin - Mermas para el Propietario
    # FIN Mermas de Fletes
    condicion_cantidad: RoundedDecimal
    tipo_flete: Optional[TipoFleteEnum] = None
    info: str
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
