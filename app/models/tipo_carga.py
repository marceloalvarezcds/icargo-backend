from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoCarga(SeleccionableMixin, Base):
    """
    Defines the tipo carga model
    """

    pass
