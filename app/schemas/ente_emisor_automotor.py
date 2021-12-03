from .pais import Pais
from .seleccionable_base_model import SeleccionableBaseModel


class EnteEmisorAutomotor(SeleccionableBaseModel):
    pais_id: int
    pais: Pais
