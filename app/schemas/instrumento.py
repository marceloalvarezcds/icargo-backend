from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum, OperacionEstadoEnum

from .date_model import Date
from .rounded_decimal_model import RoundedDecimal


class InstrumentoFormBaseModel(BaseModel):
    via_id: int
    caja_id: Optional[int]
    banco_id: Optional[int]
    fecha_instrumento: Date
    fecha_cobro: Optional[Date]
    numero_referencia: Optional[str] = None
    comentario: Optional[str] = None
    # Solo para cheque
    cheque_es_diferido: Optional[bool] = False
    cheque_fecha_vencimiento: Optional[Date] = None


class InstrumentoForm(InstrumentoFormBaseModel):
    tipo_instrumento_id: Optional[int]
    liquidacion_id: Optional[int]
    monto: RoundedDecimal
    saldo_cc: Optional[RoundedDecimal]
    tipo_cambio_moneda: RoundedDecimal
    moneda_id: int


class InstrumentoSaldoForm(InstrumentoForm):
    operacion_estado: OperacionEstadoEnum
    # Saldos
    credito: RoundedDecimal
    debito: RoundedDecimal
    saldo_confirmado: RoundedDecimal
    # Datos mostrados solo para Banco
    provision: RoundedDecimal
    saldo_provisional: RoundedDecimal


class Instrumento(InstrumentoSaldoForm):
    id: int
    liquidacion_id: int
    estado: EstadoEnum
    tipo_instrumento_id: int
    # Datos mostrados solo para Banco
    provision_rechazada: Optional[RoundedDecimal]
    # Datos calculados
    contraparte: str
    contraparte_numero_documento: str
    cuenta_descripcion: str
    moneda_id: int
    moneda_nombre: str
    moneda_simbolo: str
    saldo_total: Optional[RoundedDecimal]
    tipo_contraparte_descripcion: str
    tipo_instrumento_descripcion: str
    tipo_operacion_descripcion: str
    url: str
    via_descripcion: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
