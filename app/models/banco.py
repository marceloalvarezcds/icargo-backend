from sqlalchemy import Column, ForeignKey, Integer, Numeric, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .gestor_carga import GestorCarga
from .moneda import Moneda


class Banco(AuditMixin, Base):
    """
    Defines the banco model
    """

    __table_args__ = (
        UniqueConstraint(
            "numero_cuenta",
            "gestor_carga_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    numero_cuenta = Column(String(255))
    titular = Column(String(255))
    nombre = Column(String(255))
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    saldo_confirmado = Column(Numeric(38, 10))
    saldo_provisional = Column(Numeric(38, 10))
    instrumentos = relationship(
        "Instrumento", back_populates="banco", order_by="Instrumento.modified_at.desc()"
    )

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def moneda_simbolo(self):
        return self.moneda.simbolo

    @hybrid_property
    def info(self):
        return f"{self.nombre}: ({self.titular} - {self.numero_cuenta})"

    @hybrid_property
    def credito(self):
        if self.instrumentos:
            return sum(
                x.credito for x in self.instrumentos if x.estado != EstadoEnum.ELIMINADO.value and x.estado != EstadoEnum.ANULADO.value
            )
        return None

    @hybrid_property
    def debito(self):
        if self.instrumentos:
             return sum(
                x.debito for x in self.instrumentos if x.estado != EstadoEnum.ELIMINADO.value and x.estado != EstadoEnum.ANULADO.value
             )
        return None
