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


class MovimientoBaseModel(BaseModel):
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
    documento_fisico_oc:Optional[bool] = False
    linea_movimiento: Optional[str]


class MovimientoForm(MovimientoBaseModel):
    es_cobro: Optional[bool] = False
    es_creacion_contraparte: Optional[bool] = False


class MovimientoFleteEditForm(BaseModel):
    moneda_id: Optional[int] = None
    tarifa: Optional[RoundedDecimal] = None


class MovimientoMermaEditForm(BaseModel):
    valor: Optional[RoundedDecimal] = None
    moneda_id: Optional[int] = None
    es_porcentual: Optional[bool] = False
    tolerancia: Optional[RoundedDecimal] = None


class Movimiento(MovimientoBaseModel):
    id: int
    gestor_carga_id: int
    tipo_contraparte: TipoContraparte
    tipo_documento_relacionado: TipoDocumentoRelacionado
    cuenta: TipoCuenta
    tipo_movimiento: Optional[TipoMovimiento]
    moneda: Moneda
    # Campos calculados
    credito: RoundedDecimal
    camion_placa: Optional[str]
    chofer_nombre: Optional[str]
    chofer_numero_documento: Optional[str]
    concepto: str
    cuenta_codigo_descripcion: str
    debito: RoundedDecimal
    destino_nombre: Optional[str]
    es_cobro: bool
    fecha_pago_cobro: Optional[Date]
    flete_id: Optional[int]
    insumo_descripcion: Optional[str]
    liquidacion_fecha_creacion: Optional[Date]
    moneda_nombre: str
    moneda_simbolo: str
    monto_ml: RoundedDecimal
    origen_nombre: Optional[str]
    producto_descripcion: Optional[str]
    propietario_nombre: Optional[str]
    proveedor_nombre: Optional[str]
    punto_venta_nombre: Optional[str]
    remitente_nombre: Optional[str]
    remitente_numero_documento: Optional[str]
    saldo: RoundedDecimal
    semi_placa: Optional[str]
    tipo_contraparte_descripcion: str
    tipo_documento_relacionado_descripcion: str
    tipo_insumo_descripcion: Optional[str]
    tipo_movimiento_descripcion: Optional[str]
    tipo_operacion_descripcion: str
    # Datos de la OC
    es_flete: bool
    es_gestor: bool
    es_merma: bool
    es_propietario: bool
    can_edit_oc: bool
    cantidad_destino: Optional[RoundedDecimal] = None
    condicion_gestor_carga_moneda_id: Optional[int] = None
    condicion_gestor_carga_tarifa: Optional[RoundedDecimal] = None
    condicion_propietario_moneda_id: Optional[int] = None
    condicion_propietario_tarifa: Optional[RoundedDecimal] = None
    merma_gestor_carga_valor: Optional[RoundedDecimal] = None
    merma_gestor_carga_moneda_id: Optional[int] = None
    merma_gestor_carga_es_porcentual: Optional[bool] = False
    merma_gestor_carga_tolerancia: Optional[RoundedDecimal] = None
    merma_propietario_valor: Optional[RoundedDecimal] = None
    merma_propietario_moneda_id: Optional[int] = None
    merma_propietario_es_porcentual: Optional[bool] = False
    merma_propietario_tolerancia: Optional[RoundedDecimal] = None
    # En caso de ser movimiento de anticipo
    anticipo: Optional[OrdenCargaAnticipoRetirado] = None
    # importe de pago cobro y sentido
    monto: Optional[RoundedDecimal] = None
    es_pago_cobro: Optional[RoundedDecimal] = None
    descuento_concepto: Optional[str]
    complemento_concepto: Optional[str]

    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True


class EstadoCuentaMovimiento(Movimiento):
    pendiente: Optional[RoundedDecimal]
    en_proceso: Optional[RoundedDecimal]
    confirmado: Optional[RoundedDecimal]
    finalizado: Optional[RoundedDecimal]
