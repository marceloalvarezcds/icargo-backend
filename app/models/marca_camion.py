from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class MarcaCamion(SeleccionableMixin, Base):
    """
    Defines the marca camión model
    """

    pass
