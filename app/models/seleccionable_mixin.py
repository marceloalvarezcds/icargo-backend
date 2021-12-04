from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.enums.estado import EstadoEnum


@declarative_mixin
class SeleccionableMixin(AuditMixin):
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(255), unique=True)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
