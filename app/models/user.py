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

from .chofer import Chofer
from .gestor_carga import GestorCarga
from .propietario import Propietario
from .punto_venta import PuntoVenta
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
    email: str = Column(String(255), nullable=False)
    password: str = Column(String(255), nullable=False)
    activation_code: str = Column(String(255), index=True)
    persist_code: str = Column(String(255))
    reset_password_code: str = Column(String(255), index=True)
    is_superuser: bool = Column(Boolean, nullable=False, server_default=text("false"))
    created_ip_address: str = Column(String(255))
    last_ip_address: str = Column(String(255))
    chofer_id: int = Column(Integer, ForeignKey("chofer.id"))
    chofer: Chofer = relationship(Chofer, uselist=False, foreign_keys=[chofer_id])
    gestor_carga_id: int = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga: GestorCarga = relationship(GestorCarga, uselist=False)
    propietario_id: int = Column(Integer, ForeignKey("propietario.id"))
    propietario: Propietario = relationship(
        Propietario, uselist=False, foreign_keys=[propietario_id]
    )
    punto_venta_id: int = Column(Integer, ForeignKey("punto_venta.id"))
    punto_venta: PuntoVenta = relationship(PuntoVenta, uselist=False)
    is_admin: bool = Column(Boolean, nullable=False, server_default=text("false"))
    estado: EstadoEnum = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    user_roles: List["UserRol"] = relationship(
        "UserRol", back_populates="user", cascade="all, delete-orphan"
    )

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def is_admin_descripcion(self):
        return "Si" if self.is_admin else "No"


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
