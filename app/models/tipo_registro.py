from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoRegistro(SeleccionableMixin, Base):
    """
    Defines the tipo registro model
    """

    pass
