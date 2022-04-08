from decimal import Decimal

from .seleccionable_base_model import SeleccionableBaseModel


class TipoIva(SeleccionableBaseModel):
    pais_id: int
    iva: Decimal
    # Campos calculados
    pais_nombre: str
    pais_nombre_corto: str
