from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoIncidente(SeleccionableMixin, Base):
    """
    Defines the tipo insumo model
    """

    pass
