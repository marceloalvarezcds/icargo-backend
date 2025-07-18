from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from sqlalchemy.orm import relationship  # type: ignore
from app.models.gestor_carga import GestorCarga
from sqlalchemy import (  # type: ignore
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
class ComentarioFlota(AuditMixin, Base):
    __tablename__ = "comentarios_flota"

    id = Column(Integer, primary_key=True, index=True)
    comentable_type = Column(String(50), nullable=False)
    comentable_id = Column(Integer, nullable=False)
    comentario = Column(String(255))
    tipo_evento = Column(String(100))
    archivo = Column(String(255))
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)


    @hybrid_property
    def gestor_carga_nombre(self):
        return self.gestor_carga.nombre
