
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin
from .tipo_insumo import TipoInsumo
from .unidad import Unidad


class Insumo(SeleccionableMixin, Base):
    """
    Defines the insumo model
    """

    tipo_id = Column(Integer, ForeignKey("tipo_insumo.id"))
    tipo = relationship(TipoInsumo, uselist=False)
    unidad_id = Column(Integer, ForeignKey("unidad.id"))
    unidad = relationship(Unidad, uselist=False)
    punto_ventas = relationship("InsumoPuntoVenta", back_populates="insumo")
    fecha_creacion = Column(DateTime)
    marca = Column(String(100))

    @hybrid_property
    def tipo_descripcion(self):
        return self.tipo.descripcion

    @hybrid_property
    def unidad_descripcion(self):
        return self.unidad.descripcion

    @hybrid_property
    def unidad_abreviatura(self):
        return self.unidad.abreviatura
