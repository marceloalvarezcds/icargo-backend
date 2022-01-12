from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoComprobante(SeleccionableMixin, Base):
    """
    Defines the tipo comprobante model
    """

    pass
