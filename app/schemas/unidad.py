from .rounded_decimal_model import RoundedDecimal
from .seleccionable_base_model import SeleccionableBaseModel


class Unidad(SeleccionableBaseModel):
    abreviatura: str
    conversion_kg: RoundedDecimal
