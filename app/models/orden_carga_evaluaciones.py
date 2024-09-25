from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base
from .orden_carga import OrdenCarga
from .tipo_incidente import TipoIncidente


class OrdenCargaEvaluacionesHistorial(AuditMixin, Base):
    """
    Defines the orden carga - evaluaciones historial model
    """

    __tablename__ = 'orden_carga_evaluaciones_historial'

    id = Column(Integer, primary_key=True)
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(
        OrdenCarga, uselist=False, back_populates="evaluaciones_historial"
    )
    comentario = Column(String(255))
    created_by = Column(String(100))  
    modified_by = Column(String(100))  
    
    tipo_incidente_id = Column(Integer, ForeignKey("tipo_incidente.id"))
    tipo_incidente = relationship(TipoIncidente, uselist=False)
    
    comentarios = Column(String(255))

    # Hybrid properties for accessing related data
    @hybrid_property
    def tipo_incidente_nombre(self):
        return self.tipo_incidente.descripcion

   