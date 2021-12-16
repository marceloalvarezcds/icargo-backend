from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    text,
)
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .flete import Flete
from .moneda import Moneda
from .tipo_concepto_complemento import TipoConceptoComplemento


class FleteComplemento(AuditMixin, Base):
    """
    Defines the flete - complemento model
    """

    __table_args__ = (
        UniqueConstraint(
            "concepto_id",
            "propietario_moneda_id",
            "propietario_monto",
            "remitente_moneda_id",
            "remitente_monto",
            "flete_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    concepto_id = Column(Integer, ForeignKey("tipo_concepto_complemento.id"))
    concepto = relationship(TipoConceptoComplemento, uselist=False)
    detalle = Column(Text)
    habilitar_cobro_remitente = Column(Boolean, server_default=text("false"))
    anticipado = Column(Boolean, server_default=text("false"))
    # INICIO Monto a pagar al Propietario
    propietario_monto = Column(Numeric(38, 10))
    propietario_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    propietario_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[propietario_moneda_id]
    )
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_monto = Column(Numeric(38, 10))
    remitente_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    remitente_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[remitente_moneda_id]
    )
    # FIN Monto a cobrar al Remitente
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False, back_populates="complementos")
