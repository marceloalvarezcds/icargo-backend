from sqlalchemy import Column, Numeric, String  # type: ignore

from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class Unidad(SeleccionableMixin, Base):
    """
    Defines the unidad model
    """

    abreviatura = Column(String(255))
    conversion_kg = Column(Numeric(38, 10))
