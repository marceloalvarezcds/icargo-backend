from sqlalchemy import Column, ForeignKey, Integer, Numeric  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .flete_anticipo import FleteAnticipo
from .orden_carga import OrdenCarga
from .orden_carga_anticipo_porcentaje import OrdenCargaAnticipoPorcentaje


class OrdenCargaAnticipoSaldo(AuditMixin, Base):
    """
    Defines the orden carga - anticipo saldo model
    """

    __table_args__ = (UniqueConstraint("flete_anticipo_id", "orden_carga_id"),)
    id = Column(Integer, primary_key=True)
    flete_anticipo_id = Column(Integer, ForeignKey("flete_anticipo.id"))
    flete_anticipo = relationship(FleteAnticipo, uselist=False, back_populates="saldos")
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(OrdenCarga, uselist=False, back_populates="saldos")
    orden_carga_anticipo_porcentaje_id = Column(
        Integer, ForeignKey("orden_carga_anticipo_porcentaje.id")
    )
    orden_carga_anticipo_porcentaje = relationship(
        OrdenCargaAnticipoPorcentaje, uselist=False, back_populates="saldos"
    )
    total_anticipo = Column(Numeric(38, 10))  # cantidad_nomidada * porcentaje
    # total_anticipo_ml = Column(Numeric(38, 10))
    total_complemento = Column(Numeric(38, 10))
    total_retirado = Column(Numeric(38, 10))
    # total_retirado_ml = Column(Numeric(38, 10))
    saldo = Column(Numeric(38, 10))
    # saldo_ml = Column(Numeric(38, 10))

    @hybrid_property
    def cantidad_nominada(self):
        return self.orden_carga.cantidad_nominada

    @hybrid_property
    def concepto(self):
        return self.flete_anticipo.concepto

    @hybrid_property
    def porcentaje(self):
        return (
            self.orden_carga_anticipo_porcentaje.porcentaje
            if self.orden_carga_anticipo_porcentaje.porcentaje
            else 0
        )

    @hybrid_property
    def total_disponible(self):
        return self.total_anticipo + self.total_complemento

    @hybrid_property
    def flete_anticipo_id_property(self):
        return self.flete_anticipo.flete_id
