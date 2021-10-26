from sqlalchemy import Column, Integer, String  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum


class Rol(AuditMixin, Base):
    """
    Defines the rol model
    """

    id = Column(Integer, primary_key=True)
    codigo = Column(String(255), unique=True)
    descripcion = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
