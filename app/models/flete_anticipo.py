from sqlalchemy import Column, ForeignKey, Integer, Numeric  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .flete import Flete
from .tipo_anticipo import TipoAnticipo
from .tipo_insumo import TipoInsumo


class FleteAnticipo(AuditMixin, Base):
    """
    Defines the flete - anticipo model
    """

    __table_args__ = (UniqueConstraint("tipo_id", "flete_id", "tipo_insumo_id"),)
    id = Column(Integer, primary_key=True)
    tipo_id = Column(Integer, ForeignKey("tipo_anticipo.id"))
    tipo = relationship(TipoAnticipo, uselist=False)
    tipo_insumo_id = Column(Integer, ForeignKey("tipo_insumo.id"))
    tipo_insumo = relationship(TipoInsumo, uselist=False)
    porcentaje = Column(Numeric(38, 10))
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False, back_populates="anticipos")
    anticipos = relationship(
        "OrdenCargaAnticipoRetirado", back_populates="flete_anticipo"
    )
    saldos = relationship("OrdenCargaAnticipoSaldo", back_populates="flete_anticipo")

    @hybrid_property
    def concepto(self):
        return (
            self.tipo_insumo_descripcion if self.tipo_insumo else self.tipo_descripcion
        )

    @hybrid_property
    def tipo_descripcion(self):
        return self.tipo.descripcion

    @hybrid_property
    def tipo_insumo_descripcion(self):
        return self.tipo_insumo.descripcion if self.tipo_insumo else None
