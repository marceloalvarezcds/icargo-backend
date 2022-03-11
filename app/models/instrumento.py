from sqlalchemy import (  # type: ignore
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum, OperacionEstadoEnum
from app.enums.tipo_cuenta import TipoCuentaEnum

from .banco import Banco
from .caja import Caja
from .liquidacion import Liquidacion
from .tipo_instrumento import TipoInstrumento


class Instrumento(AuditMixin, Base):
    """
    Defines the instrumento model
    """

    id = Column(Integer, primary_key=True)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    caja_id = Column(Integer, ForeignKey("caja.id"))
    caja = relationship(Caja, uselist=False, back_populates="instrumentos")
    banco_id = Column(Integer, ForeignKey("banco.id"))
    banco = relationship(Banco, uselist=False, back_populates="instrumentos")
    liquidacion_id = Column(Integer, ForeignKey("liquidacion.id"))
    liquidacion = relationship(
        Liquidacion, uselist=False, back_populates="instrumentos"
    )
    fecha_instrumento = Column(DateTime)
    credito = Column(Numeric(38, 10))
    debito = Column(Numeric(38, 10))
    saldo_confirmado = Column(Numeric(38, 10))
    # Datos mostrados solo para Banco
    provision = Column(Numeric(38, 10))
    saldo_provisional = Column(Numeric(38, 10))
    tipo_instrumento_id = Column(Integer, ForeignKey("tipo_instrumento.id"))
    tipo_instrumento = relationship(TipoInstrumento, uselist=False)
    operacion_estado = Column(
        String(255), server_default=OperacionEstadoEnum.EMITIDO.value
    )
    operacion_numero_documento = Column(String(255))
    operacion_descripcion = Column(Text)

    @hybrid_property
    def contraparte(self):
        return self.liquidacion.contraparte

    @hybrid_property
    def contraparte_numero_documento(self):
        return self.liquidacion.contraparte_numero_documento

    @hybrid_property
    def cuenta(self):
        return self.caja if self.caja else self.banco

    @hybrid_property
    def moneda(self):
        return self.cuenta.moneda

    @hybrid_property
    def moneda_id(self):
        return self.moneda.id

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
    def tipo_cuenta(self):
        return TipoCuentaEnum.CAJA if self.caja else TipoCuentaEnum.BANCO

    @hybrid_property
    def tipo_instrumento_descripcion(self):
        return self.tipo_instrumento.descripcion

    @hybrid_property
    def url(self):
        return ""
