from sqlalchemy import (  # type: ignore
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    text,
)
from sqlalchemy.sql.elements import and_ # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Numeric  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import (
    EstadoEnum,
    LiquidacionEstadoEnum,
    LiquidacionEtapaEnum,
    TipoContraparteEnum
)

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
    pago_cobro = Column(Numeric(38, 10))
    es_pago_cobro = Column(String(10))
    aprobado_at = Column(DateTime)
    user_aprueba = Column(String(100))
    punto_venta_id = Column(Integer, ForeignKey("punto_venta.id"))
    saldo_cc = Column(Numeric(38, 10))
    tipo_mov_liquidacion = Column(String(20))
    es_orden_pago = Column(Boolean, server_default=text("false"))
    observacion = Column(Text)

    # Listas
    movimientos = relationship(
        "Movimiento",
        back_populates="liquidacion",
        order_by="Movimiento.created_at"
    )
    instrumentos = relationship(
        "Instrumento", back_populates="liquidacion", order_by="Instrumento.modified_at"
    )
    facturas = relationship(
        "Factura",
        back_populates="liquidacion",
        order_by="Factura.modified_at",
        primaryjoin="and_(Liquidacion.id == Factura.liquidacion_id, Factura.estado=='Activo')",
    )

    @hybrid_property
    def es_cobro(self):
        #return self.movimientos_saldo > 0
        #return self.pago_cobro > 0
        return self.es_pago_cobro == 'PAGO'

    @hybrid_property
    def esta_pagado(self):
        return not self.saldo_residual > 0

    @hybrid_property
    def movimientos_saldo(self):
        return sum(
            x.saldo_ml for x in self.movimientos if x.estado != EstadoEnum.ELIMINADO.value and x.estado != EstadoEnum.ANULADO.value
        )

    @hybrid_property
    def saldo_anticipos_combustible(self):
        return sum(
            x.saldo_ml
            for x in self.movimientos
            if x.estado not in [EstadoEnum.ELIMINADO.value, EstadoEnum.ANULADO.value]
            and x.tipo_movimiento.descripcion == 'Anticipo'
            and x.tipo_insumo_descripcion == 'COMBUSTIBLE'
        )

    @hybrid_property
    def saldo_anticipos_efectivo(self):
        return sum(
            x.saldo_ml
            for x in self.movimientos
            if x.estado not in [EstadoEnum.ELIMINADO.value, EstadoEnum.ANULADO.value]
            and x.tipo_movimiento.descripcion == 'Anticipo'
            and x.tipo_insumo_descripcion != 'COMBUSTIBLE'
        )


    @hybrid_property
    def saldo_anticipos_complemento_descuento(self):
        return sum(
            x.saldo_ml
            for x in self.movimientos
            if x.estado not in [EstadoEnum.ELIMINADO.value, EstadoEnum.ANULADO.value]
            and x.tipo_movimiento.descripcion in ['Complemento', 'Descuento']
        )

    @hybrid_property
    def saldo_anticipos_flete(self):
        return sum(
            x.saldo_ml
            for x in self.movimientos
            if x.estado not in [EstadoEnum.ELIMINADO.value, EstadoEnum.ANULADO.value]
            and x.tipo_movimiento.descripcion == 'Flete'
        )

    @hybrid_property
    def saldo_anticipos_merma(self):
        return sum(
            x.saldo_ml
            for x in self.movimientos
            if x.estado not in [EstadoEnum.ELIMINADO.value, EstadoEnum.ANULADO.value]
            and x.tipo_movimiento.descripcion == 'Merma'
        )

    @hybrid_property
    def saldo_anticipos_otro(self):
        return sum(
            x.saldo_ml
            for x in self.movimientos
            if x.estado not in [EstadoEnum.ELIMINADO.value, EstadoEnum.ANULADO.value]
            and x.tipo_movimiento.descripcion == 'Otro'
        )


    @hybrid_property
    def credito(self):
        return self.movimientos_saldo if self.movimientos_saldo > 0 else 0

    @hybrid_property
    def debito(self):
        return self.movimientos_saldo * -1 if self.movimientos_saldo < 0 else 0

    @hybrid_property
    def instrumentos_saldo(self):
        return abs(sum(
            x.monto_ml for x in self.instrumentos if x.operacion_estado != EstadoEnum.RECHAZADO.value and x.operacion_estado != EstadoEnum.ANULADO.value
        ))

    @hybrid_property
    def saldo(self):
        return self.credito - self.debito

    @hybrid_property
    def saldo_residual(self):
        if self.es_orden_pago:
            return abs(self.pago_cobro) - self.instrumentos_saldo
        else:
            return abs(self.movimientos_saldo) - self.instrumentos_saldo


    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def moneda_simbolo(self):
        return self.moneda.simbolo

    @hybrid_property
    def tipo_contraparte_descripcion(self):
        return self.tipo_contraparte.descripcion

    @hybrid_property
    def tipo_operacion_descripcion(self):
        return "Cobro" if self.es_cobro else "Pago"

    @hybrid_property
    def url(self):
        return ""

    @hybrid_property
    def tipo_contraparte_descripcion(self):
        return self.tipo_contraparte.descripcion

    @hybrid_property
    def es_chofer(self):
        return (
            self.tipo_contraparte_descripcion == TipoContraparteEnum.CHOFER.value
            and self.chofer is not None
        )

    @hybrid_property
    def es_propietario(self):
        return (
            self.tipo_contraparte_descripcion == TipoContraparteEnum.PROPIETARIO.value
            and self.propietario is not None
        )

    @hybrid_property
    def es_proveedor(self):
        return (
            self.tipo_contraparte_descripcion == TipoContraparteEnum.PROVEEDOR.value
            and self.proveedor is not None
        )

    @hybrid_property
    def es_gestor(self):
        return (
            self.tipo_contraparte_descripcion == TipoContraparteEnum.REMITENTE.value
            and self.remitente is not None
        )

    @hybrid_property
    def movimientos_activos(self):
        if self.movimientos:
            return [movimiento for movimiento in self.movimientos if movimiento.estado != 'Anulado']
        else:
            return []


    @hybrid_property
    def contraparte_id(self):
        if self.es_propietario:
            return self.propietario_id
        elif self.es_gestor:
            return self.remitente_id
        elif self.es_proveedor:
            return self.proveedor_id
        elif self.es_chofer:
            return self.chofer_id
        else:
            return self.id
