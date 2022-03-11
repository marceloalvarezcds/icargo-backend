from sqlalchemy import (  # type: ignore
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum, TipoContraparteEnum, TipoMovimientoEnum

from .gestor_carga import GestorCarga
from .liquidacion import Liquidacion
from .moneda import Moneda
from .orden_carga import OrdenCarga
from .orden_carga_anticipo_retirado import OrdenCargaAnticipoRetirado
from .orden_carga_complemento import OrdenCargaComplemento
from .orden_carga_descuento import OrdenCargaDescuento
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
    estado = Column(String(255), server_default=EstadoEnum.PENDIENTE.value)
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

    @hybrid_property
    def credito(self):
        return self.monto if self.monto > 0 else 0

    @hybrid_property
    def camion_placa(self):
        return self.orden_carga.camion_placa

    @hybrid_property
    def chofer_nombre(self):
        return self.orden_carga.camion_chofer_nombre

    @hybrid_property
    def chofer_numero_documento(self):
        return self.orden_carga.camion_chofer_numero_documento

    @hybrid_property
    def concepto(self):
        return self.tipo_movimiento.descripcion

    @hybrid_property
    def cuenta_descripcion(self):
        return self.cuenta.descripcion

    @hybrid_property
    def debito(self):
        return self.monto if self.monto < 0 else 0

    @hybrid_property
    def destino_nombre(self):
        return self.orden_carga.destino_nombre

    @hybrid_property
    def detalle(self):
        if self.tipo_movimiento_descripcion == TipoMovimientoEnum.ANTICIPO.value:
            return self.anticipo.detalle
        elif self.tipo_movimiento_descripcion == TipoMovimientoEnum.FLETE.value:
            if (
                self.tipo_contraparte_descripcion
                == TipoContraparteEnum.PROPIETARIO.value
            ):
                return self.orden_carga.flete_propietario_detalle
            return self.orden_carga.flete_gestor_carga_detalle
        elif self.tipo_movimiento_descripcion == TipoMovimientoEnum.COMPLEMENTO.value:
            if (
                self.tipo_contraparte_descripcion
                == TipoContraparteEnum.PROPIETARIO.value
            ):
                return self.complemento.propietario_detalle
            return self.complemento.remitente_detalle
        elif self.tipo_movimiento_descripcion == TipoMovimientoEnum.DESCUENTO.value:
            if (
                self.tipo_contraparte_descripcion
                == TipoContraparteEnum.PROPIETARIO.value
            ):
                return self.descuento.propietario_detalle
            return self.descuento.proveedor_detalle
        elif self.tipo_movimiento_descripcion == TipoMovimientoEnum.MERMA.value:
            if (
                self.tipo_contraparte_descripcion
                == TipoContraparteEnum.PROPIETARIO.value
            ):
                return self.orden_carga.merma_propietario_detalle
            return self.orden_carga.merma_gestor_carga_detalle
        return ""

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
