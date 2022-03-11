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

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.utils import number_format

from .moneda import Moneda
from .orden_carga import OrdenCarga
from .tipo_concepto_complemento import TipoConceptoComplemento


class OrdenCargaComplemento(AuditMixin, Base):
    """
    Defines the orden carga - complemento model
    """

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
    # propietario_tipo_cambio_moneda = Column(Numeric(38, 10))
    # propietario_fecha_cambio_moneda = Column(
    #     DateTime, server_default=text("CURRENT_TIMESTAMP")
    # )
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_monto = Column(Numeric(38, 10))
    remitente_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    remitente_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[remitente_moneda_id]
    )
    # remitente_tipo_cambio_moneda = Column(Numeric(38, 10))
    # remitente_fecha_cambio_moneda = Column(
    #     DateTime, server_default=text("CURRENT_TIMESTAMP")
    # )
    # FIN Monto a cobrar al Remitente
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(OrdenCarga, uselist=False, back_populates="complementos")
    flete_id = Column(Integer, ForeignKey("flete.id"))

    @hybrid_property
    def anticipado_descripcion(self):
        return "Si" if self.anticipado else "No"

    @hybrid_property
    def concepto_descripcion(self):
        return self.concepto.descripcion

    @hybrid_property
    def gestor_carga_moneda_simbolo(self):
        return self.orden_carga.gestor_carga_moneda_simbolo

    @hybrid_property
    def propietario_detalle(self):
        return f"Monto: {number_format(self.propietario_monto)}{self.propietario_moneda_simbolo}"  # || Tipo de Cambio: 250,0{self.gestor_carga_moneda_simbolo}/{self.propietario_moneda_simbolo}"  # noqa

    @hybrid_property
    def propietario_moneda_nombre(self):
        return self.propietario_moneda.nombre

    @hybrid_property
    def propietario_moneda_simbolo(self):
        return self.propietario_moneda.simbolo

    @hybrid_property
    def remitente_detalle(self):
        return f"Monto: {number_format(self.remitente_monto)}{self.remitente_moneda_simbolo}"  # || Tipo de Cambio: 250,0{self.gestor_carga_moneda_simbolo}/{self.remitente_moneda_simbolo}"  # noqa

    @hybrid_property
    def remitente_moneda_nombre(self):
        return self.remitente_moneda.nombre

    @hybrid_property
    def remitente_moneda_simbolo(self):
        return self.remitente_moneda.simbolo
