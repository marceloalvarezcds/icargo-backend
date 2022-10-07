from typing import Optional

from .seleccionable_base_model import SeleccionableBaseModel, SeleccionableFormBaseModel


class TipoCuenta(SeleccionableBaseModel):
    pass


class TipoCuentaForm(SeleccionableFormBaseModel):
    tipo_documento_relacionado_id: Optional[int] = None
