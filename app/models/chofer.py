from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .ciudad import Ciudad
from .gestor_carga import GestorCarga
from .pais import Pais
from .tipo_documento import TipoDocumento
from .tipo_registro import TipoRegistro
from .user import User


class Chofer(AuditMixin, Base):
    """
    Defines the chofer model
    """

    __table_args__ = (
        UniqueConstraint(
            "tipo_documento_id",
            "pais_emisor_documento_id",
            "numero_documento",
        ),
    )
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    tipo_documento_id = Column(Integer, ForeignKey("tipo_documento.id"))
    tipo_documento = relationship(TipoDocumento, uselist=False)
    pais_emisor_documento_id = Column(Integer, ForeignKey("pais.id"))
    pais_emisor_documento = relationship(Pais, uselist=False)
    numero_documento = Column(String(255))
    ruc = Column(String(255))
    digito_verificador = Column(String(2))
    fecha_nacimiento = Column(DateTime)
    gestor_cuenta_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_cuenta = relationship(GestorCarga, uselist=False)
    oficial_cuenta_id = Column(Integer, ForeignKey("user.id"))
    oficial_cuenta = relationship(User, uselist=False)
    foto_documento_frente = Column(String(255))
    foto_documento_reverso = Column(String(255))
    foto_perfil = Column(String(255))
    es_propietario = Column(Boolean, nullable=False, server_default=text("false"))
    # inicio registro
    ciudad_emisor_registro_id = Column(Integer, ForeignKey("ciudad.id"))
    ciudad_emisor_registro = relationship(
        Ciudad, uselist=False, foreign_keys=[ciudad_emisor_registro_id]
    )
    tipo_registro_id = Column(Integer, ForeignKey("tipo_registro.id"))
    tipo_registro = relationship(TipoRegistro, uselist=False)
    numero_registro = Column(String(255))
    vencimiento_registro = Column(DateTime)
    foto_registro_frente = Column(String(255))
    foto_registro_reverso = Column(String(255))
    # fin registro
    estado = Column(String(255), server_default=EstadoEnum.PENDIENTE.value)
    telefono = Column(String(25))
    email = Column(String(50))
    direccion = Column(String(255))
    ciudad_id = Column(Integer, ForeignKey("ciudad.id"))
    ciudad = relationship(Ciudad, uselist=False, foreign_keys=[ciudad_id])
    puede_recibir_anticipos = Column(Boolean, server_default=text("true"))
    gestores = relationship("GestorCargaChofer", back_populates="chofer")

    @hybrid_property
    def ciudad_nombre(self):
        return self.ciudad.nombre if self.ciudad else None

    @hybrid_property
    def gestor_cuenta_nombre(self):
        return self.gestor_cuenta.nombre if self.gestor_cuenta else None

    @hybrid_property
    def localidad_nombre(self):
        return self.ciudad.localidad.nombre if self.ciudad else None

    @hybrid_property
    def localidad_emisor_registro(self):
        return (
            self.ciudad_emisor_registro.localidad
            if self.ciudad_emisor_registro
            else None
        )

    @hybrid_property
    def localidad_emisor_registro_id(self):
        return (
            self.ciudad_emisor_registro.localidad_id
            if self.ciudad_emisor_registro
            else None
        )

    @hybrid_property
    def oficial_cuenta_nombre(self):
        return (
            f"{self.oficial_cuenta.first_name} {self.oficial_cuenta.last_name}"
            if self.oficial_cuenta
            else None
        )

    @hybrid_property
    def pais_nombre(self):
        return self.ciudad.localidad.pais.nombre if self.ciudad else None

    @hybrid_property
    def pais_nombre_corto(self):
        return self.ciudad.localidad.pais.nombre_corto if self.ciudad else None

    @hybrid_property
    def pais_emisor_documento_nombre(self):
        return self.pais_emisor_documento.nombre

    @hybrid_property
    def pais_emisor_documento_nombre_corto(self):
        return self.pais_emisor_documento.nombre_corto

    @hybrid_property
    def pais_emisor_registro(self):
        return (
            self.localidad_emisor_registro.pais
            if self.localidad_emisor_registro
            else None
        )

    @hybrid_property
    def pais_emisor_registro_id(self):
        return (
            self.localidad_emisor_registro.pais_id
            if self.localidad_emisor_registro
            else None
        )

    @hybrid_property
    def tipo_documento_descripcion(self):
        return self.tipo_documento.descripcion
