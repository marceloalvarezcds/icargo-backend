from sqlalchemy import Column, Integer, String, Text
from app.audits.audit_mixin import AuditMixin
from app.database.base import Base


class ComentarioFlota(AuditMixin, Base):
    __tablename__ = "comentarios_flota"

    id = Column(Integer, primary_key=True, index=True)
    comentable_type = Column(String(50), nullable=False)
    comentable_id = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=False)
    tipo_evento = Column(String(100))
    archivo = Column(Text)


