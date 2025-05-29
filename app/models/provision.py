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
from sqlalchemy.orm import relationship  # type: ignore
from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import (
    MovimientoEstadoEnum
)
from .chofer import Chofer
from .gestor_carga import GestorCarga
from .moneda import Moneda
from .orden_carga import OrdenCarga
from .orden_carga_complemento import OrdenCargaComplemento
from .orden_carga_descuento import OrdenCargaDescuento
from .propietario import Propietario
from .proveedor import Proveedor
from .remitente import Remitente
from .tipo_contraparte import TipoContraparte
from .tipo_cuenta import TipoCuenta
from .tipo_documento_relacionado import TipoDocumentoRelacionado
from .tipo_movimiento import TipoMovimiento


class Provision(AuditMixin, Base):
    # Preguntar por Nº Doc. Fiscal entre los campos de Movimiento
    id = Column(Integer, primary_key=True)
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
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
    #es_editable = Column(Boolean, server_default=text("false"))
    fecha = Column(DateTime)
    detalle = Column(Text)
    tipo_movimiento_info = Column(Text)
    monto = Column(Numeric(38, 10))
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    tipo_cambio_moneda = Column(Numeric(38, 10))
    fecha_cambio_moneda = Column(DateTime)

    # En caso de ser movimiento de complemento o descuento
    complemento_id = Column(Integer, ForeignKey("orden_carga_complemento.id", onupdate="CASCADE", ondelete="CASCADE"))
    complemento = relationship(OrdenCargaComplemento, uselist=False)
    descuento_id = Column(Integer, ForeignKey("orden_carga_descuento.id", onupdate="CASCADE", ondelete="CASCADE"))
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
    punto_venta_id = Column(Integer)
    linea_movimiento = Column(String(20))
