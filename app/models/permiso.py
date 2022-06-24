from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.sql.schema import Index, UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base


class Permiso(AuditMixin, Base):
    """
    Defines the permiso model
    """

    __table_args__ = (
        Index("permiso_modulo_modelo_accion_index", "modulo", "modelo", "accion"),
        UniqueConstraint("modelo", "accion"),
    )
    id = Column(Integer, primary_key=True)
    accion = Column(String(255))
    modelo = Column(String(255))
    modulo = Column(String(255))
    modelo_titulo = Column(String(255))
    descripcion = Column(String(255))
