from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import MovimientoEstadoEnum
from app.enums.tipo_contraparte import TipoContraparteEnum
from app.enums.tipo_movimiento import TipoMovimientoEnum

from .chofer import Chofer
from .gestor_carga import GestorCarga
from .liquidacion import Liquidacion
from .moneda import Moneda
from .orden_carga import OrdenCarga
from .orden_carga_anticipo_retirado import OrdenCargaAnticipoRetirado
from .orden_carga_complemento import OrdenCargaComplemento
from .orden_carga_descuento import OrdenCargaDescuento
from .propietario import Propietario
from .proveedor import Proveedor
from .remitente import Remitente
from .tipo_contraparte import TipoContraparte
from .tipo_cuenta import TipoCuenta
from .tipo_documento_relacionado import TipoDocumentoRelacionado
from .tipo_movimiento import TipoMovimiento


class Movimiento(AuditMixin, Base):
    """
    Defines the movimiento model
    """

    # Preguntar por Nº Doc. Fiscal entre los campos de Movimiento
    id = Column(Integer, primary_key=True)
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    liquidacion_id = Column(Integer, ForeignKey("liquidacion.id"))
    liquidacion = relationship(Liquidacion, uselist=False, back_populates="movimientos")
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(OrdenCarga, uselist=False)
    estado = Column(String(255), server_default=MovimientoEstadoEnum.PENDIENTE.value)
    tipo_contraparte_id = Column(Integer, ForeignKey("tipo_contraparte.id"))
    tipo_contraparte = relationship(TipoContraparte, uselist=False)
    contraparte = Column(String(255))
    contraparte_numero_documento = Column(String(255))  # documento fiscal
    tipo_documento_relacionado_id = Column(
        Integer, ForeignKey("tipo_documento_relacionado.id")
    )
    tipo_documento_relacionado = relationship(TipoDocumentoRelacionado, uselist=False)
    numero_documento_relacionado = Column(String(255))
    cuenta_id = Column(Integer, ForeignKey("tipo_cuenta.id"))
    cuenta = relationship(TipoCuenta, uselist=False)
    tipo_movimiento_id = Column(Integer, ForeignKey("tipo_movimiento.id"))
    tipo_movimiento = relationship(TipoMovimiento, uselist=False)  # concepto
    es_editable = Column(Boolean, server_default=text("false"))
    fecha = Column(DateTime)
    detalle = Column(Text)
    monto = Column(Numeric(38, 10))
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    tipo_cambio_moneda = Column(Numeric(38, 10))
    fecha_cambio_moneda = Column(DateTime)
    # En caso de ser movimiento de anticipo
    anticipo_id = Column(Integer, ForeignKey("orden_carga_anticipo_retirado.id"))
    anticipo = relationship(OrdenCargaAnticipoRetirado, uselist=False)
    # En caso de ser movimiento de complemento o descuento
    complemento_id = Column(Integer, ForeignKey("orden_carga_complemento.id"))
    complemento = relationship(OrdenCargaComplemento, uselist=False)
    descuento_id = Column(Integer, ForeignKey("orden_carga_descuento.id"))
    descuento = relationship(OrdenCargaDescuento, uselist=False)
    # IDs para referencia a las tablas de las contraparte
    chofer_id = Column(Integer, ForeignKey("chofer.id"))
    chofer = relationship(Chofer, uselist=False)
    propietario_id = Column(Integer, ForeignKey("propietario.id"))
    propietario = relationship(Propietario, uselist=False)
    proveedor_id = Column(Integer, ForeignKey("proveedor.id"))
    proveedor = relationship(Proveedor, uselist=False)
    remitente_id = Column(Integer, ForeignKey("remitente.id"))
    remitente = relationship(Remitente, uselist=False)

    @hybrid_property
    def credito(self):
        return self.monto if self.monto > 0 else 0

    @hybrid_property
    def camion_placa(self):
        return self.orden_carga.camion_placa if self.orden_carga else None

    @hybrid_property
    def chofer_nombre(self):
        return self.orden_carga.camion_chofer_nombre if self.orden_carga else None

    @hybrid_property
    def chofer_numero_documento(self):
        return (
            self.orden_carga.camion_chofer_numero_documento
            if self.orden_carga
            else None
        )

    @hybrid_property
    def concepto(self):
        return self.tipo_movimiento.descripcion

    @hybrid_property
    def cuenta_descripcion(self):
        return self.cuenta.descripcion

    @hybrid_property
    def debito(self):
        return self.monto * -1 if self.monto < 0 else 0

    @hybrid_property
    def destino_nombre(self):
        return self.orden_carga.destino_nombre

    @hybrid_property
    def es_cobro(self):
        return self.monto > 0

    @hybrid_property
    def fecha_pago_cobro(self):
        return self.liquidacion.fecha_pago_cobro

    @hybrid_property
    def flete_id(self):
        return self.orden_carga.flete_id

    @hybrid_property
    def insumo_descripcion(self):
        return self.anticipo.insumo_descripcion if self.anticipo else None

    @hybrid_property
    def liquidacion_fecha(self):
        return self.liquidacion.fecha_aprobacion

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def monto_ml(self):
        return self.monto * self.tipo_cambio_moneda

    @hybrid_property
    def moneda_simbolo(self):
        return self.moneda.simbolo

    @hybrid_property
    def origen_nombre(self):
        return self.orden_carga.origen_nombre

    @hybrid_property
    def producto_descripcion(self):
        return self.orden_carga.flete_producto_descripcion

    @hybrid_property
    def propietario_nombre(self):
        return self.orden_carga.camion_propietario_nombre

    @hybrid_property
    def proveedor_nombre(self):
        return self.anticipo.proveedor_nombre if self.anticipo else None

    @hybrid_property
    def remitente_nombre(self):
        return self.orden_carga.flete_remitente_nombre

    @hybrid_property
    def remitente_numero_documento(self):
        return self.orden_carga.flete_remitente_numero_documento

    @hybrid_property
    def saldo(self):
        return self.credito - self.debito

    @hybrid_property
    def semi_placa(self):
        return self.orden_carga.semi_placa

    @hybrid_property
    def tipo_contraparte_descripcion(self):
        return self.tipo_contraparte.descripcion

    @hybrid_property
    def tipo_documento_relacionado_descripcion(self):
        return self.tipo_documento_relacionado.descripcion

    @hybrid_property
    def tipo_insumo_descripcion(self):
        return self.anticipo.tipo_insumo_descripcion if self.anticipo else None

    @hybrid_property
    def tipo_movimiento_descripcion(self):
        return self.tipo_movimiento.descripcion

    @hybrid_property
    def tipo_operacion_descripcion(self):
        return "Cobro" if self.es_cobro else "Pago"

    # Campos editables de la OC desde el movimiento
    @hybrid_property
    def es_flete(self):
        return self.tipo_movimiento_descripcion == TipoMovimientoEnum.FLETE.value

    @hybrid_property
    def es_gestor(self):
        return self.tipo_contraparte_descripcion == TipoContraparteEnum.REMITENTE.value

    @hybrid_property
    def es_merma(self):
        return self.tipo_movimiento_descripcion == TipoMovimientoEnum.MERMA.value

    @hybrid_property
    def es_propietario(self):
        return (
            self.tipo_contraparte_descripcion == TipoContraparteEnum.PROPIETARIO.value
        )

    @hybrid_property
    def can_edit_oc(self):
        return (
            (
                self.estado != MovimientoEstadoEnum.FINALIZADO
                and (self.es_flete or self.es_merma)
                and (self.es_gestor or self.es_propietario)
            )
            if self.orden_carga
            else False
        )

    @hybrid_property
    def cantidad_destino(self):
        return self.orden_carga.cantidad_destino if self.orden_carga else None

    @hybrid_property
    def condicion_gestor_carga_moneda_id(self):
        return (
            self.orden_carga.condicion_gestor_carga_moneda_id
            if self.orden_carga
            else None
        )

    @hybrid_property
    def condicion_gestor_carga_tarifa(self):
        return (
            self.orden_carga.condicion_gestor_carga_tarifa if self.orden_carga else None
        )

    @hybrid_property
    def condicion_propietario_moneda_id(self):
        return (
            self.orden_carga.condicion_propietario_moneda_id
            if self.orden_carga
            else None
        )

    @hybrid_property
    def condicion_propietario_tarifa(self):
        return (
            self.orden_carga.condicion_propietario_tarifa if self.orden_carga else None
        )

    @hybrid_property
    def merma_gestor_carga_valor(self):
        return self.orden_carga.merma_gestor_carga_valor if self.orden_carga else None

    @hybrid_property
    def merma_gestor_carga_moneda_id(self):
        return (
            self.orden_carga.merma_gestor_carga_moneda_id if self.orden_carga else None
        )

    @hybrid_property
    def merma_gestor_carga_es_porcentual(self):
        return (
            self.orden_carga.merma_gestor_carga_es_porcentual
            if self.orden_carga
            else None
        )

    @hybrid_property
    def merma_gestor_carga_tolerancia(self):
        return (
            self.orden_carga.merma_gestor_carga_tolerancia if self.orden_carga else None
        )

    @hybrid_property
    def merma_propietario_valor(self):
        return self.orden_carga.merma_propietario_valor if self.orden_carga else None

    @hybrid_property
    def merma_propietario_moneda_id(self):
        return (
            self.orden_carga.merma_propietario_moneda_id if self.orden_carga else None
        )

    @hybrid_property
    def merma_propietario_es_porcentual(self):
        return (
            self.orden_carga.merma_propietario_es_porcentual
            if self.orden_carga
            else None
        )

    @hybrid_property
    def merma_propietario_tolerancia(self):
        return (
            self.orden_carga.merma_propietario_tolerancia if self.orden_carga else None
        )

    # TERMINA Campos editables de la OC desde el movimiento
