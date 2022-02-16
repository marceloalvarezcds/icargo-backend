from decimal import Decimal

from pydantic import BaseModel

from .date_model import Date


class OrdenCargaAnticipoSaldoForm(BaseModel):
    flete_anticipo_id: int
    orden_carga_id: int
    total_anticipo: Decimal
    total_complemento: Decimal
    total_retirado: Decimal
    saldo: Decimal


class OrdenCargaAnticipoSaldo(OrdenCargaAnticipoSaldoForm):
    id: int
    cantidad_nominada: Decimal
    concepto: str
    porcentaje: Decimal
    total_disponible: Decimal
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
