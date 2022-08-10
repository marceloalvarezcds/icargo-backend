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
            "tipo_persona_id",
            "ruc",
        ),
    )
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    tipo_persona_id = Column(Integer, ForeignKey("tipo_persona.id"))
    tipo_persona = relationship(TipoPersona, uselist=False)
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
    ciudad = relationship(Ciudad, uselist=False)
    chofer_id = Column(Integer, ForeignKey("chofer.id"))
    chofer = relationship(Chofer, uselist=False)
    puede_recibir_anticipos = Column(Boolean, server_default=text("true"))
    contactos = relationship(
        "PropietarioContactoGestorCarga", back_populates="propietario"
    )
    gestores = relationship("GestorCargaPropietario", back_populates="propietario")

    @hybrid_property
    def ciudad_nombre(self):
        return self.ciudad.nombre if self.ciudad else None

    @hybrid_property
    def gestor_cuenta_nombre(self):
        return self.gestor_cuenta.nombre

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
