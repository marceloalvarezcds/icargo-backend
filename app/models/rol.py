from typing import List

from sqlalchemy import (  # type: ignore
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .gestor_carga import GestorCarga
from .permiso import Permiso


class Rol(AuditMixin, Base):
    """
    Defines the rol model
    """

    __table_args__ = (
        UniqueConstraint(
            "descripcion",
            "gestor_carga_id",
        ),
    )
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    codigo: str = Column(String(255))
    descripcion: str = Column(String(255))
    gestor_carga_id: int = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga: GestorCarga = relationship(GestorCarga, uselist=False)
    estado: EstadoEnum = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    roles_permisos: List["RolPermiso"] = relationship(
        "RolPermiso", back_populates="rol", cascade="all, delete-orphan"
    )

    @hybrid_property
    def permisos(self) -> List[Permiso]:
        return [x.permiso for x in self.roles_permisos]


class RolPermiso(AuditMixin, Base):
    """
    Defines the rol_permiso model
    """

    __table_args__ = (
        UniqueConstraint(
            "rol_id",
            "permiso_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    rol_id = Column(Integer, ForeignKey("rol.id", ondelete="CASCADE"))
    rol: Rol = relationship(Rol, uselist=False)
    permiso_id = Column(Integer, ForeignKey("permiso.id", ondelete="CASCADE"))
    permiso: Permiso = relationship(Permiso, uselist=False)
