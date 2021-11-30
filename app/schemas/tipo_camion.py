from typing import Optional

from .seleccionable_base_model import SeleccionableBaseModel


class TipoCamion(SeleccionableBaseModel):
    tipo_imagen: Optional[str] = None
