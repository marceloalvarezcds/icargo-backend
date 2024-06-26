from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, validator

from app.enums.estado import EstadoEnum

from .date_model import Date
from .instrumento import Instrumento
from .rounded_decimal_model import RoundedDecimal


class CajaForm(BaseModel):
    nombre: str
    moneda_id: int
    gestor_carga_id: Optional[int]


class Caja(CajaForm):
    id: int
    gestor_carga_id: int
    estado: EstadoEnum
    instrumentos: List[Instrumento]
    # Campos calculados
    credito: Optional[RoundedDecimal]
    debito: Optional[RoundedDecimal]
    moneda_nombre: str
    moneda_simbolo: str
    saldo_confirmado: Optional[RoundedDecimal]
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
        validate_assignment = True

    @validator("saldo_confirmado")
    def set_saldo_confirmado(cls, saldo_confirmado):
        return saldo_confirmado or Decimal(0)
    
    @validator("credito")
    def set_credito(cls, credito):
        return credito or Decimal(0)    
    
    @validator("debito")
    def set_debito(cls, debito):
        return debito or Decimal(0)      