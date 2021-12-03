from sqlalchemy import Column, ForeignKey, Integer  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .pais import Pais
from .seleccionable_mixin import SeleccionableMixin


class EnteEmisorAutomotor(SeleccionableMixin, Base):
    """
    Defines the ente emisor automotor model
    """

    pais_id = Column(Integer, ForeignKey("pais.id"))
    pais = relationship(Pais, uselist=False)
