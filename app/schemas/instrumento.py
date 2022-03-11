from decimal import Decimal

from pydantic import BaseModel

from app.enums import EstadoEnum, OperacionEstadoEnum

from .date_model import Date


class InstrumentoForm(BaseModel):
    caja_id: int
    banco_id: int
    liquidacion_id: int
    tipo_operacion_id: int
    moneda_id: int
    credito: Decimal
    debito: Decimal
    # Datos mostrados solo para Banco
    fecha_instrumento: Date
    tipo_instrumento_id: int
    operacion_numero_documento: str
    operacion_descripcion: str
    operacion_fecha: Date


class Instrumento(InstrumentoForm):
    id: int
    url: str
    estado: EstadoEnum
    # Datos mostrados solo para Banco
    operacion_estado: OperacionEstadoEnum
    # Datos calculados
    contraparte: str
    contraparte_numero_documento: str
    moneda_nombre: str
    moneda_simbolo: str
    saldo_confirmado: Decimal
    saldo_provisional: Decimal
    saldo_total: Decimal
    tipo_contraparte_descripcion: str
    tipo_instrumento_descripcion: str
    tipo_operacion_descripcion: str

    class Config:
        orm_mode = True
        use_enum_values = True
