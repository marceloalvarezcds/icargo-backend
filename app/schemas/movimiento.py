from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .date_model import Date
from .moneda import Moneda
from .tipo_contraparte import TipoContraparte
from .tipo_cuenta import TipoCuenta
from .tipo_documento_relacionado import TipoDocumentoRelacionado
from .tipo_movimiento import TipoMovimiento


class MovimientoForm(BaseModel):
    gestor_carga_id: Optional[int]
    liquidacion_id: Optional[int]
    orden_carga_id: Optional[int]
    tipo_contraparte_id: int
    contraparte: str
    contraparte_numero_documento: str
    tipo_documento_relacionado_id: int
    numero_documento_relacionado: Optional[int]
    cuenta_id: int
    tipo_movimiento_id: int
    monto: Decimal
    moneda_id: int
    tipo_cambio_moneda: Decimal
    fecha_cambio_moneda: Date
    # En caso de ser movimiento de anticipo
    anticipo_id: Optional[int]
    # En caso de ser movimiento de complemento o descuento
    complemento_id: Optional[int]
    descuento_id: Optional[int]


class Movimiento(MovimientoForm):
    id: int
    gestor_carga_id: int
    estado: EstadoEnum
    tipo_contraparte: TipoContraparte
    tipo_documento_relacionado: TipoDocumentoRelacionado
    cuenta: TipoCuenta
    tipo_movimiento: TipoMovimiento
    moneda: Moneda
    # Campos calculados
    credito: Decimal
    camion_placa: str
    chofer_nombre: str
    chofer_numero_documento: str
    concepto: str
    cuenta_descripcion: str
    debito: Decimal
    destino_nombre: str
    detalle: Optional[str]
    es_cobro: bool
    fecha_pago_cobro: Optional[Date]
    flete_id: Optional[int]
    insumo_descripcion: Optional[str]
    liquidacion_fecha: Optional[str]
    moneda_nombre: str
    moneda_simbolo: str
    monto_ml: Decimal
    origen_nombre: Optional[str]
    producto_descripcion: Optional[str]
    propietario_nombre: Optional[str]
    proveedor_nombre: Optional[str]
    remitente_nombre: Optional[str]
    remitente_numero_documento: Optional[str]
    saldo: Decimal
    semi_placa: Optional[str]
    tipo_contraparte_descripcion: str
    tipo_documento_relacionado_descripcion: str
    tipo_insumo_descripcion: Optional[str]
    tipo_movimiento_descripcion: str
    tipo_operacion_descripcion: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
