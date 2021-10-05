from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base


class Pais(AuditMixin, Base):
    """
    Defines the pais model
    """

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    nombre_corto = Column(String(255), unique=True)
    localidades = relationship("Localidad", back_populates="pais")
