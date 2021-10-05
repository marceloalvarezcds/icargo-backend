from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.models.pais import Pais


class Localidad(AuditMixin, Base):
    """
    Defines the localidad model
    """

    __table_args__ = (UniqueConstraint("nombre", "pais_id"),)
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    pais_id = Column(Integer, ForeignKey("pais.id"))
    pais = relationship(Pais, back_populates="localidades", uselist=False)
    ciudades = relationship("Ciudad", back_populates="localidad")
