from sqlalchemy import Column, String  # type: ignore

from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class Color(SeleccionableMixin, Base):
    """
    Defines the color model
    """

    color = Column(String(30))
