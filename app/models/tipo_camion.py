from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoCamion(SeleccionableMixin, Base):
    """
    Defines the tipo camión model
    """

    pass
