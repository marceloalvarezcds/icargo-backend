from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
    Numeric,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum
from app.models.composicion_juridica import ComposicionJuridica
from app.models.tipo_documento import TipoDocumento

from .chofer import Chofer
from .ciudad import Ciudad
from .gestor_carga import GestorCarga
from .pais import Pais
from .tipo_persona import TipoPersona
from .user import User


class Propietario(AuditMixin, Base):
    """
    Defines the propietario model
    """

    __table_args__ = (
        UniqueConstraint(
            "composicion_juridica_id",
            "ruc",
        ),
    )
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    composicion_juridica_id = Column(Integer, ForeignKey("composicion_juridica.id"))
    composicion_juridica = relationship(ComposicionJuridica, uselist=False)

    tipo_documento_propietario_id = Column(Integer, ForeignKey("tipo_documento.id"))
    tipo_documento = relationship(TipoDocumento, uselist=False)

    nombre_corto = Column(String(255))
    ruc = Column(String(255))
    digito_verificador = Column(String(2))
    pais_origen_id = Column(Integer, ForeignKey("pais.id"))
    pais_origen = relationship(Pais, uselist=False)
    fecha_nacimiento = Column(DateTime)
    gestor_cuenta_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_cuenta = relationship(GestorCarga, uselist=False)
    oficial_cuenta_id = Column(Integer, ForeignKey("user.id"))
    oficial_cuenta = relationship(User, uselist=False)
    foto_documento_frente = Column(String(255))
    foto_documento_reverso = Column(String(255))
    foto_perfil = Column(String(255))
    es_chofer = Column(Boolean, nullable=False, server_default=text("false"))
    estado = Column(String(255), server_default=EstadoEnum.PENDIENTE.value)
    telefono = Column(String(25))
    email = Column(String(50))
    direccion = Column(String(255))
    ciudad_id = Column(Integer, ForeignKey("ciudad.id"))
    ciudad: Ciudad = relationship(Ciudad, uselist=False)
    chofer_id = Column(Integer, ForeignKey("chofer.id"))
    chofer: Chofer = relationship(Chofer, uselist=False)
    puede_recibir_anticipos = Column(Boolean, server_default=text("true"))
    is_propietario_condicionado = Column(Boolean, nullable=False, server_default=text("false"))
    contactos = relationship(
        "PropietarioContactoGestorCarga", back_populates="propietario"
    )
    gestores = relationship("GestorCargaPropietario", back_populates="propietario")

    promedio_propietario_gestor = Column(Numeric(38, 1), nullable=True)
    promedio_propietario_general = Column(Numeric(38, 1), nullable=True)
    cantidad_propietario_evaluaciones = Column(Numeric(38, 1), nullable=True)
    cantidad_propietario_evaluaciones_gestor = Column(Numeric(38, 1), nullable=True)

    @hybrid_property
    def ciudad_nombre(self):
        return self.ciudad.nombre if self.ciudad else None

    @hybrid_property
    def gestor_cuenta_nombre(self):
        return self.gestor_cuenta.nombre if self.gestor_cuenta else None

    @hybrid_property
    def info(self):
        return f"{self.nombre} - {self.ruc}"

    @hybrid_property
    def localidad_nombre(self):
        return self.ciudad.localidad.nombre if self.ciudad else None

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
    def pais_origen_nombre(self):
        return self.pais_origen.nombre

    @hybrid_property
    def pais_origen_nombre_corto(self):
        return self.pais_origen.nombre_corto

    @hybrid_property
    def tipo_persona_descripcion(self):
        return self.tipo_persona.descripcion

    @hybrid_property
    def tipo_documento_id(self):
        return self.chofer.tipo_documento_id if self.chofer else None

    @hybrid_property
    def tipo_documento(self):
        return self.chofer.tipo_documento if self.chofer else None

    @hybrid_property
    def pais_emisor_documento_id(self):
        return self.chofer.pais_emisor_documento_id if self.chofer else None

    @hybrid_property
    def pais_emisor_documento(self):
        return self.chofer.pais_emisor_documento if self.chofer else None

    @hybrid_property
    def numero_documento(self):
        return self.chofer.numero_documento if self.chofer else None

    @hybrid_property
    def foto_documento_frente_chofer(self):
        return self.chofer.foto_documento_frente if self.chofer else None

    @hybrid_property
    def foto_documento_reverso_chofer(self):
        return self.chofer.foto_documento_reverso if self.chofer else None

    @hybrid_property
    def ciudad_emisor_registro(self):
        return self.chofer.ciudad_emisor_registro if self.chofer else None

    @hybrid_property
    def ciudad_emisor_registro_id(self):
        return self.ciudad_emisor_registro.id if self.ciudad_emisor_registro else None

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
            self.localidad_emisor_registro.id
            if self.localidad_emisor_registro
            else None
        )

    @hybrid_property
    def pais_emisor_registro(self):
        return (
            self.localidad_emisor_registro.pais
            if self.localidad_emisor_registro
            else None
        )

    @hybrid_property
    def pais_emisor_registro_id(self):
        return self.pais_emisor_registro.id if self.pais_emisor_registro else None

    @hybrid_property
    def tipo_registro(self):
        return self.chofer.tipo_registro if self.chofer else None

    @hybrid_property
    def tipo_registro_id(self):
        return self.chofer.tipo_registro_id if self.chofer else None

    @hybrid_property
    def numero_registro(self):
        return self.chofer.numero_registro if self.chofer else None

    @hybrid_property
    def vencimiento_registro(self):
        return self.chofer.vencimiento_registro if self.chofer else None

    @hybrid_property
    def foto_registro_frente(self):
        return self.chofer.foto_registro_frente if self.chofer else None

    @hybrid_property
    def foto_registro_reverso(self):
        return self.chofer.foto_registro_reverso if self.chofer else None
