from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .centro_operativo_clasificacion import CentroOperativoClasificacion
from .ciudad import Ciudad


class CentroOperativo(AuditMixin, Base):
    """
    Defines the centro operativo model
    """

    __table_args__ = (
        UniqueConstraint(
            "nombre",
            "clasificacion_id",
            "ciudad_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    nombre_corto = Column(String(255))
    logo = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    telefono = Column(String(25))
    email = Column(String(50))
    pagina_web = Column(String(255))
    direccion = Column(String(255))
    latitud = Column(DECIMAL)
    longitud = Column(DECIMAL)
    clasificacion_id = Column(Integer, ForeignKey("centro_operativo_clasificacion.id"))
    clasificacion = relationship(CentroOperativoClasificacion, uselist=False)
    ciudad_id = Column(Integer, ForeignKey("ciudad.id"))
    ciudad = relationship(Ciudad, uselist=False)
    contactos = relationship(
        "CentroOperativoContactoGestorCarga", back_populates="centro_operativo"
    )
    gestores = relationship(
        "GestorCargaCentroOperativo", back_populates="centro_operativo"
    )

    @hybrid_property
    def clasificacion_nombre(self):
        return self.clasificacion.nombre

    @hybrid_property
    def ciudad_nombre(self):
        return self.ciudad.nombre

    @hybrid_property
    def localidad_nombre(self):
        return self.ciudad.localidad.nombre

    @hybrid_property
    def pais_id(self):
        return self.ciudad.localidad.pais_id

    @hybrid_property
    def pais_nombre(self):
        return self.ciudad.localidad.pais.nombre

    @hybrid_property
    def pais_nombre_corto(self):
        return self.ciudad.localidad.pais.nombre_corto
