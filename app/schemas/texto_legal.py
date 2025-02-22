
from typing import Optional
from app.enums import EstadoEnum
from .seleccionable_base_model import SeleccionableBaseModel, SeleccionableFormBaseModel


class TextoLegalBaseModel(SeleccionableFormBaseModel):
    titulo: str
    gestor_carga_id: Optional[int]


class TextoLegalModel(SeleccionableBaseModel):
    titulo: str
    gestor_carga_id: Optional[int]


class TextoLegalForm(TextoLegalBaseModel):
    alias: Optional[str] = None

