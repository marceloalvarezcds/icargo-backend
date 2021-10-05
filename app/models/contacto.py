from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base


class Contacto(AuditMixin, Base):
    """
    Defines the contacto model
    """

    __table_args__ = (UniqueConstraint("nombre", "apellido", "telefono", "email"),)
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    apellido = Column(String(255))
    telefono = Column(String(25))
    email = Column(String(50))
