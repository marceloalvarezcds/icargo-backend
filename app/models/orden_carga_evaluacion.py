from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base
from .orden_carga import OrdenCarga
from .tipo_incidente import TipoIncidente
from app.audits.audit_mixin import AuditMixin

class OrdenCargaEvaluacionesHistorial(AuditMixin, Base):
    """
    Defines the orden carga - evaluaciones historial model
    """

    __tablename__ = 'orden_carga_evaluaciones_historial'

    id = Column(Integer, primary_key=True)
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(
        "OrdenCarga", uselist=False, back_populates="evaluaciones_historial"
    )
    comentario = Column(String(255))
    tipo_incidente_id = Column(Integer, ForeignKey("tipo_incidente.id"))
    tipo_incidente = relationship("TipoIncidente", uselist=False)
    
    comentarios = Column(String(255))
    gestor_carga_id = Column(Integer)
    camion_id = Column(Integer)
    semi_id = Column(Integer) 
    propietario_id = Column(Integer)
    chofer_id = Column(Integer)
    concepto = Column(String(255))
    nota = Column(String(255))
    origen_id = Column(Integer)
    destino_id = Column(Integer)
    producto_id = Column(Integer)
    tracto_rating = Column(Integer, nullable=True)
    semi_rating = Column(Integer, nullable=True)
    chofer_rating = Column(Integer, nullable=True)
    propietario_rating = Column(Integer, nullable=True)
    carga_rating = Column(Integer, nullable=True)
    descarga_rating = Column(Integer, nullable=True)

    # Hybrid properties for accessing related data
    @hybrid_property
    def tipo_incidente_nombre(self):
        return self.tipo_incidente.descripcion
    
    @hybrid_property
    def oc_camion_placa(self):
        return self.orden_carga.camion_placa

    @hybrid_property
    def oc_semi_placa(self):
        return self.orden_carga.semi_placa
    
    @hybrid_property
    def oc_chofer_nombre(self):
        return self.orden_carga.combinacion_chofer_nombre
    
    @hybrid_property
    def oc_beneficiario_nombre(self):
        return self.orden_carga.camion_beneficiario_nombre


   