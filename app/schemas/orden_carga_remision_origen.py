from typing import Optional

from pydantic import BaseModel

from .date_model import Date
from .rounded_decimal_model import RoundedDecimal


class OrdenCargaRemisionOrigenForm(BaseModel):
    numero_documento: str
    fecha: Date
    cantidad: RoundedDecimal
    unidad_id: int
    foto_documento: Optional[str] = None
    orden_carga_id: int


class OrdenCargaRemisionOrigen(OrdenCargaRemisionOrigenForm):
    id: int
    cantidad_kg: RoundedDecimal
    unidad_abreviatura: str
    unidad_descripcion: str
    gestor_carga_moneda_nombre: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
