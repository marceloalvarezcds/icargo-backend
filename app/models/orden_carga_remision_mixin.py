from sqlalchemy import Column, DateTime, Integer, Numeric, String  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore

from app.audits.audit_mixin import AuditMixin


@declarative_mixin
class OrdenCargaRemisionMixin(AuditMixin):
    """
    Defines the orden carga - remision mixin
    """

    id = Column(Integer, primary_key=True)
    numero_documento = Column(String(255), unique=True)
    fecha = Column(DateTime)
    cantidad = Column(Numeric(38, 10))
    foto_documento = Column(String(255))
