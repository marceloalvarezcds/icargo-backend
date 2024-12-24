from pydantic import BaseModel

from .date_model import Date
from .rounded_decimal_model import RoundedDecimal


class OrdenCargaAnticipoSaldoForm(BaseModel):
    flete_anticipo_id: int
    orden_carga_id: int
    orden_carga_anticipo_porcentaje_id: int
    total_anticipo: RoundedDecimal
    total_complemento: RoundedDecimal
    total_retirado: RoundedDecimal
    saldo: RoundedDecimal


class OrdenCargaAnticipoSaldo(OrdenCargaAnticipoSaldoForm):
    id: int
    cantidad_nominada: RoundedDecimal
    concepto: str
    porcentaje: RoundedDecimal
    total_disponible: RoundedDecimal
    flete_anticipo_id_property: int
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
