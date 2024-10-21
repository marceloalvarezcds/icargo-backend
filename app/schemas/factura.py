from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum
from app.schemas.rounded_decimal_model import RoundedDecimal

from .date_model import Date


class FacturaForm(BaseModel):
    liquidacion_id: int
    moneda_id: int
    iva_id: int
    numero_factura: str
    timbrado: str
    contribuyente: str
    ruc: str
    monto: RoundedDecimal
    iva: RoundedDecimal
    retencion: RoundedDecimal
    fecha_vencimiento: Date
    fecha_factura: Date
    tipo_contraparte_id: int
    contraparte_id: int
    iva_incl: Optional[bool] = None
    es_pago: Optional[bool] = None
    es_cobro: Optional[bool] = None

class FacturaResponse(BaseModel):
    liquidacion_id: int
    moneda_id: int
    iva_id: int
    numero_factura: str
    timbrado: Optional[str]
    contribuyente: Optional[str]
    ruc: Optional[str]
    monto: RoundedDecimal
    iva: Optional[RoundedDecimal]
    retencion: Optional[RoundedDecimal]
    fecha_vencimiento: Date
    fecha_factura: Optional[Date]
    tipo_contraparte_id: int
    contraparte_id: int
    iva_incl: Optional[bool] = None
    es_pago: Optional[bool] = None
    es_cobro: Optional[bool] = None


class Factura(FacturaResponse):
    id: int
    liquidacion_id: int
    estado: EstadoEnum
    foto: Optional[str]
    contraparte: str
    contraparte_numero_documento: str
    iva_descripcion: str
    moneda_nombre: str
    moneda_simbolo: str
    tipo_contraparte_descripcion: str
    tipo_operacion_descripcion: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
