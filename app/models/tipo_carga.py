from sqlalchemy import Column, Integer, String  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum


class TipoCarga(AuditMixin, Base):
    """
    Defines the tipo carga model
    """

    id = Column(Integer, primary_key=True)
    descripcion = Column(String(255), unique=True)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
