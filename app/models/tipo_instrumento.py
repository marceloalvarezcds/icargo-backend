from sqlalchemy import Column, ForeignKey, Integer  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .instrumento_via import InstrumentoVia
from .seleccionable_mixin import SeleccionableMixin


class TipoInstrumento(SeleccionableMixin, Base):
    """
    Defines the tipo instrumento model
    """

    via_id = Column(Integer, ForeignKey("instrumento_via.id"))
    via = relationship(InstrumentoVia, uselist=False)
