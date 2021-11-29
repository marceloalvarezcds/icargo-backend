from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin


class TipoPersona(SeleccionableMixin, Base):
    """
    Defines the tipo persona model
    """

    pass
