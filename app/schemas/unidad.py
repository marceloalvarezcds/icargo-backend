from decimal import Decimal

from .seleccionable_base_model import SeleccionableBaseModel


class Unidad(SeleccionableBaseModel):
    conversion_kg: Decimal
