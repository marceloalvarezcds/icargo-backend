from pydantic import BaseModel, validator

from app.schemas.estado_cuenta import EstadoCuentaForm
from decimal import Decimal
from typing import List, Optional
from app.enums import LiquidacionEstadoEnum, LiquidacionEtapaEnum
from .date_model import Date
from .factura import Factura
from .instrumento import Instrumento, InstrumentoForm
from .moneda import Moneda
from .movimiento import Movimiento
from .rounded_decimal_model import RoundedDecimal
from .tipo_contraparte import TipoContraparte
from app.enums.tipo_liquidacion import TipoLiquidacion

class LiquidacionNewMovimientosForm(BaseModel):
    movimientos: List[Movimiento]
    cabecera: EstadoCuentaForm
    monto: Optional[RoundedDecimal]
    es_pago_cobro: Optional[str]
    tipo_mov_liquidacion: Optional[str] = "EFECTIVO"
    moneda: Moneda
    es_orden_pago: bool
    observacion: Optional[str]


class LiquidacionCabeceraMovimientosForm(BaseModel):
    movimientos: List[Movimiento]
    cabecera: EstadoCuentaForm
    monto: Optional[RoundedDecimal]
    es_pago_cobro: Optional[str]
    tipo_mov_liquidacion: Optional[str]
    moneda: Moneda
    es_orden_pago: bool
    observacion: Optional[str]


class LiquidacionAddMovimientosForm(BaseModel):
    movimientos: List[Movimiento]
    cabecera: Optional[EstadoCuentaForm]
    monto: Optional[RoundedDecimal]
    es_pago_cobro: Optional[str]
    tipo_mov_liquidacion: Optional[str]


class LiquidacionAddInstrumentosForm(BaseModel):
    instrumentos: List[InstrumentoForm]


class LiquidacionForm(BaseModel):
    tipo_contraparte_id: int
    contraparte: str
    contraparte_numero_documento: str
    moneda_id: int
    # IDs para referencia a las tablas de las contraparte
    chofer_id: Optional[int]
    gestor_carga_id: Optional[int]
    propietario_id: Optional[int]
    proveedor_id: Optional[int]
    remitente_id: Optional[int]
    punto_venta_id: Optional[int]
    monto: Optional[RoundedDecimal]
    es_pago_cobro: Optional[str]
    saldo_cc: Optional[RoundedDecimal]
    tipo_mov_liquidacion: str
    es_orden_pago: bool
    tipo_cambio_moneda: Optional[RoundedDecimal]
    observacion: Optional[str]


class Liquidacion(LiquidacionForm):
    id: int
    tipo_contraparte: TipoContraparte
    fecha_pago_cobro: Optional[Date]
    estado: LiquidacionEstadoEnum
    etapa: LiquidacionEtapaEnum
    moneda: Moneda
    comentarios: Optional[str]
    movimientos: List[Movimiento]
    movimientos_activos: List[Movimiento]
    instrumentos: List[Instrumento]
    facturas: List[Factura]
    # Campos calculados
    credito: RoundedDecimal
    es_cobro: bool
    esta_pagado: Optional[bool] = False
    debito: RoundedDecimal
    instrumentos_saldo: Optional[RoundedDecimal]
    moneda_nombre: str
    moneda_simbolo: str
    movimientos_saldo: RoundedDecimal
    saldo_anticipos_combustible: Optional[RoundedDecimal] = None
    saldo_anticipos_efectivo: Optional[RoundedDecimal] = None
    saldo_anticipos_complemento_descuento: Optional[RoundedDecimal] = None
    saldo_anticipos_flete: Optional[RoundedDecimal] = None
    saldo_anticipos_merma: Optional[RoundedDecimal] = None
    saldo_anticipos_otro: Optional[RoundedDecimal] = None
    saldo: RoundedDecimal
    saldo_residual: Optional[RoundedDecimal] = None
    tipo_contraparte_descripcion: str
    tipo_operacion_descripcion: str
    url: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date
    pago_cobro: Optional[RoundedDecimal]
    aprobado_at: Optional[Date]
    user_aprueba: Optional[str]


    class Config:
        orm_mode = True
        use_enum_values = True

    @validator("instrumentos_saldo")
    def set_instrumentos_saldo(cls, instrumentos_saldo):
        return instrumentos_saldo or Decimal(0)


class LiquidacionSometer(BaseModel):
    comentario: Optional[str]
    monto: Optional[RoundedDecimal]



class LiquidacionReport(BaseModel):
    movimientos: List[Movimiento]
    orden_carga_id: int
    total_orden_carga: RoundedDecimal
