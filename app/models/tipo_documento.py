from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoDocumento(SeleccionableMixin, Base):
    """
    Defines the tipo documento model
    """

    pass
