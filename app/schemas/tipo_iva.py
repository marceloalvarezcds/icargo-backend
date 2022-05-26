from .rounded_decimal_model import RoundedDecimal
from .seleccionable_base_model import SeleccionableBaseModel


class TipoIva(SeleccionableBaseModel):
    pais_id: int
    iva: RoundedDecimal
    # Campos calculados
    pais_nombre: str
    pais_nombre_corto: str
