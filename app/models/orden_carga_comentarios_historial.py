from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from .orden_carga import OrdenCarga


class OrdenCargaComentariosHistorial(AuditMixin, Base):
    """
    Defines the orden carga - comentarios historial model
    """

    __tablename__ = "orden_carga_comentarios_historial"

    id = Column(Integer, primary_key=True)
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))  # Puede ser NULL

    comentario = Column(String(255))  # Puede ser NULL
    created_by = Column(String(100))  # Puede ser NULL
    modified_by = Column(String(100))  # Puede ser NULL

    # Definición de la relación
    orden_carga = relationship("OrdenCarga", back_populates="comentario")  # Usar cadena para evitar problemas



