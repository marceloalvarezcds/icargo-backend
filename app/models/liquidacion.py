from sqlalchemy import (  # type: ignore
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum, LiquidacionEstadoEnum, LiquidacionEtapaEnum

from .chofer import Chofer
from .gestor_carga import GestorCarga
from .moneda import Moneda
from .propietario import Propietario
from .proveedor import Proveedor
from .remitente import Remitente
from .tipo_contraparte import TipoContraparte


class Liquidacion(AuditMixin, Base):
    """
    Defines the liquidacion model
    """

    id = Column(Integer, primary_key=True)
    tipo_contraparte_id = Column(Integer, ForeignKey("tipo_contraparte.id"))
    tipo_contraparte = relationship(TipoContraparte, uselist=False)
    contraparte = Column(String(255))
    contraparte_numero_documento = Column(String(255))
    fecha_pago_cobro = Column(DateTime)
    estado = Column(String(255), server_default=LiquidacionEstadoEnum.EN_REVISION.value)
    etapa = Column(String(255), server_default=LiquidacionEtapaEnum.EN_PROCESO.value)
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    comentarios = Column(Text)
    # IDs para referencia a las tablas de las contraparte
    chofer_id = Column(Integer, ForeignKey("chofer.id"))
    chofer = relationship(Chofer, uselist=False)
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    propietario_id = Column(Integer, ForeignKey("propietario.id"))
    propietario = relationship(Propietario, uselist=False)
    proveedor_id = Column(Integer, ForeignKey("proveedor.id"))
    proveedor = relationship(Proveedor, uselist=False)
    remitente_id = Column(Integer, ForeignKey("remitente.id"))
    remitente = relationship(Remitente, uselist=False)
    # Listas
    movimientos = relationship(
        "Movimiento", back_populates="liquidacion", order_by="Movimiento.created_at"
    )
    instrumentos = relationship(
        "Instrumento", back_populates="liquidacion", order_by="Instrumento.modified_at"
    )
    facturas = relationship(
        "Factura", back_populates="liquidacion", order_by="Factura.modified_at"
    )

    @hybrid_property
    def credito(self):
        return self.movimientos_saldo if self.movimientos_saldo > 0 else 0

    @hybrid_property
    def es_cobro(self):
        return self.movimientos_saldo > 0

    @hybrid_property
    def esta_pagado(self):
        return not self.saldo_residual > 0

    @hybrid_property
    def debito(self):
        return self.movimientos_saldo * -1 if self.movimientos_saldo < 0 else 0

    @hybrid_property
    def instrumentos_saldo(self):
        return abs(
            sum(
                x.monto
                for x in self.instrumentos
                if x.estado != EstadoEnum.ELIMINADO.value
            )
        )

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def moneda_simbolo(self):
        return self.moneda.simbolo

    @hybrid_property
    def movimientos_saldo(self):
        return sum(
            x.saldo for x in self.movimientos if x.estado != EstadoEnum.ELIMINADO.value
        )

    @hybrid_property
    def saldo(self):
        return self.credito - self.debito

    @hybrid_property
    def saldo_residual(self):
        return abs(self.movimientos_saldo) - self.instrumentos_saldo

    @hybrid_property
    def tipo_contraparte_descripcion(self):
        return self.tipo_contraparte.descripcion

    @hybrid_property
    def tipo_operacion_descripcion(self):
        return "Cobro" if self.es_cobro else "Pago"

    @hybrid_property
    def url(self):
        return ""
