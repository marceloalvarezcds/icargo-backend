from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, validator

from app.enums import LiquidacionEstadoEnum, LiquidacionEtapaEnum

from .date_model import Date
from .instrumento import Instrumento, InstrumentoForm
from .moneda import Moneda
from .movimiento import Movimiento
from .tipo_contraparte import TipoContraparte


class LiquidacionAddMovimientosForm(BaseModel):
    movimientos: List[Movimiento]


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


class Liquidacion(LiquidacionForm):
    id: int
    tipo_contraparte: TipoContraparte
    fecha_pago_cobro: Optional[Date]
    estado: LiquidacionEstadoEnum
    etapa: LiquidacionEtapaEnum
    moneda: Moneda
    comentarios: Optional[str]
    movimientos: List[Movimiento]
    instrumentos: List[Instrumento]
    # Campos calculados
    credito: Decimal
    es_cobro: bool
    esta_pagado: Optional[bool] = False
    debito: Decimal
    instrumentos_saldo: Optional[Decimal]
    moneda_nombre: str
    moneda_simbolo: str
    movimientos_saldo: Decimal
    saldo: Decimal
    saldo_residual: Optional[Decimal] = Decimal(0)
    tipo_contraparte_descripcion: str
    tipo_operacion_descripcion: str
    url: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True

    @validator("instrumentos_saldo")
    def set_instrumentos_saldo(cls, instrumentos_saldo):
        return instrumentos_saldo or Decimal(0)
