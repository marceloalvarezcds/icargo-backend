from typing import Optional

from .seleccionable_base_model import SeleccionableBaseModel, SeleccionableFormBaseModel


class TipoCuenta(SeleccionableBaseModel):
    # codigo: str
    codigo_descripcion: str


class TipoCuentaForm(SeleccionableFormBaseModel):
    codigo: str
    tipo_documento_relacionado_id: Optional[int] = None
