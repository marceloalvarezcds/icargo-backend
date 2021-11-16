from sqlalchemy import Boolean, Column, Integer, String, text  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base


class Permiso(AuditMixin, Base):
    """
    Defines the permiso model
    """

    __table_args__ = (UniqueConstraint("accion", "modelo", "autorizado"),)
    id = Column(Integer, primary_key=True)
    accion = Column(String(255))
    modelo = Column(String(255))
    autorizado = Column(Boolean, nullable=False, server_default=text("true"))
    descripcion = Column(String(255))
