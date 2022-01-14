from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .centro_operativo import CentroOperativo
from .orden_carga import OrdenCarga
from .orden_carga_remision_mixin import OrdenCargaRemisionMixin
from .unidad import Unidad


class OrdenCargaRemisionDestino(OrdenCargaRemisionMixin, Base):
    """
    Defines the orden carga - remision destino model
    """

    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(
        OrdenCarga, uselist=False, back_populates="remisiones_destino"
    )
    unidad_id = Column(Integer, ForeignKey("unidad.id"))
    unidad = relationship(Unidad, uselist=False)
    numero_documento_origen = Column(String(255))
    destino_id = Column(Integer, ForeignKey("centro_operativo.id"))
    destino = relationship(CentroOperativo, uselist=False)

    @hybrid_property
    def destino_nombre(self):
        return self.destino.nombre

    @hybrid_property
    def gestor_carga_moneda_nombre(self):
        return self.orden_carga.gestor_carga_moneda_nombre

    @hybrid_property
    def unidad_abreviatura(self):
        return self.unidad.abreviatura

    @hybrid_property
    def unidad_descripcion(self):
        return self.unidad.descripcion
