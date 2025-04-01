from typing import Optional

from pydantic import BaseModel

from .rounded_decimal_model import RoundedDecimal


class OrdenCargaRemisionResultado(BaseModel):
    responsable: str
    tarifa_flete: RoundedDecimal
    total_flete: RoundedDecimal
    merma_valor: RoundedDecimal
    tolerancia: RoundedDecimal
    tolerancia_kg: RoundedDecimal
    merma: RoundedDecimal
    merma_valor_total: RoundedDecimal
    merma_valor_total_moneda_local: RoundedDecimal
    total_complemento: Optional[RoundedDecimal] = None
    total_descuento: Optional[RoundedDecimal] = None
    total_anticipo: Optional[RoundedDecimal] = None
    saldo: RoundedDecimal
    total_efectivo: Optional[RoundedDecimal] = None
    total_combustible: Optional[RoundedDecimal] = None
    saldo_bruto: Optional[RoundedDecimal] = None
    complemento_descuento: Optional[RoundedDecimal] = None
    flete_tarifa_unidad_gestor_carga: Optional[str] = None
