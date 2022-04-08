from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .date_model import Date


class FacturaForm(BaseModel):
    liquidacion_id: int
    moneda_id: int
    iva_id: int
    numero_factura: str
    monto: Decimal
    fecha_vencimiento: Date


class Factura(FacturaForm):
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
