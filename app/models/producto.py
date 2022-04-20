from sqlalchemy import Column, ForeignKey, Integer  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin
from .tipo_carga import TipoCarga


class Producto(SeleccionableMixin, Base):
    """
    Defines the producto model
    """

    tipo_carga_id = Column(Integer, ForeignKey("tipo_carga.id"))
    tipo_carga = relationship(TipoCarga, uselist=False)

    @hybrid_property
    def tipo_carga_descripcion(self):
        return self.tipo_carga.descripcion
