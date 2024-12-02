from typing import Optional
from pydantic import BaseModel
from app.enums import MovimientoEstadoEnum
from .date_model import Date
from .moneda import Moneda
from .orden_carga_anticipo_retirado import OrdenCargaAnticipoRetirado
from .rounded_decimal_model import RoundedDecimal
from .tipo_contraparte import TipoContraparte
from .tipo_cuenta import TipoCuenta
from .tipo_documento_relacionado import TipoDocumentoRelacionado
from .tipo_movimiento import TipoMovimiento


class ProvisionBaseModel(BaseModel):
    gestor_carga_id: Optional[int]
    liquidacion_id: Optional[int]
    orden_carga_id: Optional[int]
    tipo_contraparte_id: int
    contraparte_id: Optional[int]
    contraparte: str
    contraparte_numero_documento: str
    tipo_documento_relacionado_id: Optional[int]
    numero_documento_relacionado: Optional[int]
    cuenta_id: Optional[int]
    tipo_movimiento_id: Optional[int]
    es_editable: Optional[bool] = False
    estado: MovimientoEstadoEnum
    fecha: Optional[Date]
    detalle: Optional[str]
    monto: RoundedDecimal
    moneda_id: int
    tipo_cambio_moneda: Optional[RoundedDecimal]
    fecha_cambio_moneda: Optional[Date]
    # En caso de ser movimiento de anticipo
    anticipo_id: Optional[int]
    # En caso de ser movimiento de complemento o descuento
    complemento_id: Optional[int]
    descuento_id: Optional[int]
    # IDs para referencia a las tablas de las contraparte
    chofer_id: Optional[int]
    propietario_id: Optional[int]
    proveedor_id: Optional[int]
    remitente_id: Optional[int]
    punto_venta_id: Optional[int]
    es_punto_venta: Optional[bool]
    tipo_movimiento_info: Optional[str]

class ProvisionForm(ProvisionBaseModel):
    es_cobro: Optional[bool] = False
    es_creacion_contraparte: Optional[bool] = False
