from sqlalchemy import (  # type: ignore
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum

from .liquidacion import Liquidacion
from .moneda import Moneda
from .tipo_iva import TipoIva


class Factura(AuditMixin, Base):
    """
    Defines the factura model
    """

    __table_args__ = (
        UniqueConstraint(
            "liquidacion_id",
            "numero_factura",
            "moneda_id",
            "iva_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    liquidacion_id = Column(Integer, ForeignKey("liquidacion.id"))
    liquidacion = relationship(Liquidacion,
                uselist=False,
                primaryjoin="Liquidacion.id == Factura.liquidacion_id and Factura.estado=='Activo'",
                back_populates="facturas")
    numero_factura = Column(String(255))
    monto = Column(Numeric(38, 10))
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    iva_id = Column(Integer, ForeignKey("tipo_iva.id"))
    tipo_iva = relationship(TipoIva, uselist=False)
    fecha_vencimiento = Column(DateTime)
    foto = Column(String(255))

    timbrado = Column(String(30))
    contribuyente = Column(String(50))
    ruc = Column(String(255))
    fecha_factura = Column(DateTime)
    iva = Column(Numeric(38,10))
    retencion = Column(Numeric(38,10))
    iva_incluido = Column(Boolean, unique=False, default=False)
    sentido_mov_iva = Column( String(10) )
    sentido_mov_retencion = Column( String(10) )

    iva_movimiento_id = Column( Integer )
    retencion_movimiento_id = Column( Integer)

    @hybrid_property
    def contraparte(self):
        return self.liquidacion.contraparte

    @hybrid_property
    def contraparte_numero_documento(self):
        return self.liquidacion.contraparte_numero_documento

    @hybrid_property
    def iva_descripcion(self):
        return self.tipo_iva.descripcion

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def moneda_simbolo(self):
        return self.moneda.simbolo

    @hybrid_property
    def tipo_contraparte_descripcion(self):
        return self.liquidacion.tipo_contraparte_descripcion

    @hybrid_property
    def tipo_operacion_descripcion(self):
        return self.liquidacion.tipo_operacion_descripcion

    @hybrid_property
    def tipo_contraparte_id(self):
        return self.liquidacion.tipo_contraparte_id

    @hybrid_property
    def contraparte_id(self):
        return self.liquidacion.contraparte_id
