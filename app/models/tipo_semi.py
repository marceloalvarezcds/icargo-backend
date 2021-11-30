from sqlalchemy import Column, String  # type: ignore

from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoSemi(SeleccionableMixin, Base):
    """
    Defines the tipo semi model
    """

    tipo_imagen = Column(String(255))
