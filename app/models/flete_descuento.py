from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .flete import Flete
from .moneda import Moneda
from .proveedor import Proveedor
from .tipo_concepto_descuento import TipoConceptoDescuento


class FleteDescuento(AuditMixin, Base):
    """
    Defines the flete - descuento model
    """

    __table_args__ = (
        UniqueConstraint(
            "concepto_id",
            "propietario_moneda_id",
            "propietario_monto",
            "proveedor_moneda_id",
            "proveedor_monto",
            "flete_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    concepto_id = Column(Integer, ForeignKey("tipo_concepto_descuento.id"))
    concepto = relationship(TipoConceptoDescuento, uselist=False)
    detalle = Column(Text)
    habilitar_pago_proveedor = Column(Boolean, server_default=text("false"))
    anticipado = Column(Boolean, server_default=text("false"))
    # INICIO Monto a cobrar al Propietario
    propietario_monto = Column(Numeric(38, 10))
    propietario_monto_ml = Column(Numeric(38, 10)) #Calculo moneda local
    propietario_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    propietario_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[propietario_moneda_id]
    )
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_monto = Column(Numeric(38, 10))
    proveedor_monto_ml = Column(Numeric(38, 10)) #Calculo moneda local
    proveedor_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    proveedor_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[proveedor_moneda_id]
    )
    proveedor_id = Column(Integer, ForeignKey("proveedor.id"))
    proveedor = relationship(Proveedor, uselist=False)
    # FIN Monto a pagar al Proveedor
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False, back_populates="descuentos")

    @hybrid_property
    def concepto_descripcion(self):
        return self.concepto.descripcion

    @hybrid_property
    def propietario_moneda_nombre(self):
        return self.propietario_moneda.nombre

    @hybrid_property
    def propietario_moneda_simbolo(self):
        return self.propietario_moneda.simbolo

    @hybrid_property
    def proveedor_moneda_nombre(self):
        return self.proveedor_moneda.nombre

    @hybrid_property
    def proveedor_moneda_simbolo(self):
        return self.proveedor_moneda.simbolo

    @hybrid_property
    def proveedor_nombre(self):
        return self.proveedor.nombre

    @hybrid_property
    def gestor_carga_moneda_simbolo(self):
        return self.flete.gestor_carga_moneda_simbolo
