from sqlalchemy import Column, ForeignKey, Integer, Numeric  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .flete import Flete
from .tipo_anticipo import TipoAnticipo


class FleteAnticipo(AuditMixin, Base):
    """
    Defines the flete - anticipo model
    """

    __table_args__ = (UniqueConstraint("tipo_id", "flete_id"),)
    id = Column(Integer, primary_key=True)
    tipo_id = Column(Integer, ForeignKey("tipo_anticipo.id"))
    tipo = relationship(TipoAnticipo, uselist=False)
    porcentaje = Column(Numeric(38, 10))
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False, back_populates="anticipos")

    @hybrid_property
    def tipo_descripcion(self):
        return self.tipo.descripcion
