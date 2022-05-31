from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.models.localidad import Localidad


class Ciudad(AuditMixin, Base):
    """
    Defines the ciudad model
    """

    __table_args__ = (UniqueConstraint("nombre", "localidad_id"),)
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    localidad_id = Column(Integer, ForeignKey("localidad.id"))
    localidad = relationship(Localidad, back_populates="ciudades", uselist=False)

    @hybrid_property
    def localidad_nombre(self):
        return self.localidad.nombre

    @hybrid_property
    def pais_id(self):
        return self.localidad.pais_id

    @hybrid_property
    def pais_nombre(self):
        return self.localidad.pais.nombre

    @hybrid_property
    def pais_nombre_corto(self):
        return self.localidad.pais.nombre_corto
