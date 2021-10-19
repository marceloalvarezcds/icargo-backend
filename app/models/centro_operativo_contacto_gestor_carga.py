from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .cargo import Cargo
from .centro_operativo import CentroOperativo
from .contacto import Contacto
from .gestor_carga import GestorCarga


class CentroOperativoContactoGestorCarga(AuditMixin, Base):
    """
    Defines the centro operativo - contacto - gestor carga model
    """

    __table_args__ = (
        UniqueConstraint(
            "centro_operativo_id",
            "contacto_id",
            "gestor_carga_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    cargo_id = Column(Integer, ForeignKey("cargo.id"))
    cargo = relationship(Cargo, uselist=False)
    centro_operativo_id = Column(Integer, ForeignKey("centro_operativo.id"))
    centro_operativo = relationship(
        CentroOperativo, uselist=False, back_populates="contactos"
    )
    contacto_id = Column(Integer, ForeignKey("contacto.id"))
    contacto = relationship(Contacto, uselist=False)
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)

    @hybrid_property
    def cargo_descripcion(self):
        return self.cargo.descripcion

    @hybrid_property
    def contacto_nombre(self):
        return self.contacto.nombre

    @hybrid_property
    def contacto_apellido(self):
        return self.contacto.apellido

    @hybrid_property
    def contacto_telefono(self):
        return self.contacto.telefono

    @hybrid_property
    def contacto_email(self):
        return self.contacto.email
