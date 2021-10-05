from sqlalchemy import Boolean, Column, Integer, String, text  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base


class CentroOperativoClasificacion(AuditMixin, Base):
    """
    Defines the centro operativo clasificacion model
    """

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), unique=True)
    es_moderado = Column(Boolean(), server_default=text("false"))
