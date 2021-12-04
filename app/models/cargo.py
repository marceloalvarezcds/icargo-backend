from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class Cargo(SeleccionableMixin, Base):
    """
    Defines the cargo model
    """

    pass
