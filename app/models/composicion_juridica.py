from sqlalchemy import Column, Integer, String  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum


class ComposicionJuridica(AuditMixin, Base):
    """
    Defines the composicion juridica model
    """

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), unique=True)
    nombre_corto = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
