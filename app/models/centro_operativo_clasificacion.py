from sqlalchemy import Column, Integer, String  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum


class CentroOperativoClasificacion(AuditMixin, Base):
    """
    Defines the centro operativo clasificacion model
    """

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), unique=True)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
