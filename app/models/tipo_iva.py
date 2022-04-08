from sqlalchemy import Column, ForeignKey, Integer, Numeric  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .pais import Pais
from .seleccionable_mixin import SeleccionableMixin


class TipoIva(SeleccionableMixin, Base):
    """
    Defines the tipo iva model
    """

    pais_id = Column(Integer, ForeignKey("pais.id"))
    pais = relationship(Pais, uselist=False)
    iva = Column(Numeric(38, 10))

    @hybrid_property
    def pais_nombre(self):
        return self.pais.nombre

    @hybrid_property
    def pais_nombre_corto(self):
        return self.pais.nombre_corto
