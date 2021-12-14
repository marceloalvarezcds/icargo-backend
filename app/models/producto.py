from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class Producto(SeleccionableMixin, Base):
    """
    Defines the producto model
    """

    pass
