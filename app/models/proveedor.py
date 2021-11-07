from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .ciudad import Ciudad
from .composicion_juridica import ComposicionJuridica
from .tipo_documento import TipoDocumento


class Proveedor(AuditMixin, Base):
    """
    Defines the proveedor model
    """

    __table_args__ = (
        UniqueConstraint(
            "tipo_documento_id",
            "numero_documento",
        ),
    )
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    nombre_corto = Column(String(255))
    tipo_documento_id = Column(Integer, ForeignKey("tipo_documento.id"))
    tipo_documento = relationship(TipoDocumento, uselist=False)
    numero_documento = Column(String(255))
    digito_verificador = Column(String(2))
    composicion_juridica_id = Column(Integer, ForeignKey("composicion_juridica.id"))
    composicion_juridica = relationship(ComposicionJuridica, uselist=False)
    logo = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    telefono = Column(String(25))
    email = Column(String(50))
    pagina_web = Column(String(255))
    direccion = Column(String(255))
    latitud = Column(DECIMAL)
    longitud = Column(DECIMAL)
    ciudad_id = Column(Integer, ForeignKey("ciudad.id"))
    ciudad = relationship(Ciudad, uselist=False)
    contactos = relationship("ProveedorContactoGestorCarga", back_populates="proveedor")
    gestores = relationship("GestorCargaProveedor", back_populates="proveedor")

    @hybrid_property
    def ciudad_nombre(self):
        return self.ciudad.nombre

    @hybrid_property
    def composicion_juridica_nombre(self):
        return self.composicion_juridica.nombre

    @hybrid_property
    def localidad_nombre(self):
        return self.ciudad.localidad.nombre

    @hybrid_property
    def pais_nombre(self):
        return self.ciudad.localidad.pais.nombre

    @hybrid_property
    def pais_nombre_corto(self):
        return self.ciudad.localidad.pais.nombre_corto

    @hybrid_property
    def tipo_documento_descripcion(self):
        return self.tipo_documento.descripcion
