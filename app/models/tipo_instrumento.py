from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoInstrumento(SeleccionableMixin, Base):
    """
    Defines the tipo instrumento model
    """

    pass
