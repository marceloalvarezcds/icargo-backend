from typing import Optional

from .seleccionable_base_model import SeleccionableBaseModel


class TipoSemi(SeleccionableBaseModel):
    tipo_imagen: Optional[str] = None
