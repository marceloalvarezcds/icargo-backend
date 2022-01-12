from .seleccionable_base_model import SeleccionableBaseModel
from .tipo_carga import TipoCarga


class Producto(SeleccionableBaseModel):
    tipo_carga_id: int
    tipo_carga: TipoCarga
