from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class OrdenCargaRemisionResultado(BaseModel):
    responsable: str
    tarifa_flete: Decimal
    total_flete: Decimal
    merma_valor: Decimal
    tolerancia: Decimal
    tolerancia_kg: Decimal
    merma: Decimal
    merma_valor_total: Decimal
    merma_valor_total_moneda_local: Decimal
    total_complemento: Optional[Decimal] = None
    total_descuento: Optional[Decimal] = None
    total_anticipo: Optional[Decimal] = None
    saldo: Decimal
