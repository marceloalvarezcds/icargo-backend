from typing import List

from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .gestor_carga import GestorCarga
from .permiso import Permiso
from .rol import Rol


class User(AuditMixin, Base):
    """
    Defines the user model
    """

    id: int = Column(Integer, primary_key=True)
    token: str = Column(String, unique=True)
    first_name: str = Column(String(255))
    last_name: str = Column(String(255))
    username: str = Column(String(255), nullable=False, unique=True)
    surname: str = Column(String(255))
    email: str = Column(String(255), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    activation_code: str = Column(String(255), index=True)
    persist_code: str = Column(String(255))
    reset_password_code: str = Column(String(255), index=True)
    is_superuser: bool = Column(Boolean, nullable=False, server_default=text("false"))
    created_ip_address: str = Column(String(255))
    last_ip_address: str = Column(String(255))
    gestor_carga_id: int = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga: GestorCarga = relationship(GestorCarga, uselist=False)
    estado: EstadoEnum = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    user_roles: List["UserRol"] = relationship(
        "UserRol", back_populates="user", cascade="all, delete-orphan"
    )

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def roles(self) -> List[Rol]:
        return [x.rol for x in self.user_roles]

    @hybrid_property
    def permisos(self) -> List[Permiso]:
        permisos: List[Permiso] = []
        roles: List[Rol] = self.roles
        for x in roles:
            permisos.extend(x.permisos)
        return permisos


class UserRol(AuditMixin, Base):
    """
    Defines the user_rol model
    """

    __table_args__ = (
        UniqueConstraint(
            "rol_id",
            "user_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    rol_id = Column(Integer, ForeignKey("rol.id", ondelete="CASCADE"))
    rol: Rol = relationship(Rol, uselist=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user: User = relationship(User, uselist=False)
