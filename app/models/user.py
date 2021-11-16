from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.schema import Table  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .gestor_carga import GestorCarga
from .permiso import Permiso
from .rol import Rol

user_rol_table = Table(
    "user_rol",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("rol_id", ForeignKey("rol.id")),
)

user_permiso_table = Table(
    "user_permiso",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("permiso_id", ForeignKey("permiso.id")),
)


class User(AuditMixin, Base):
    """
    Defines the user model
    """

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String(255), nullable=False, unique=True)
    surname = Column(String(255))
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    activation_code = Column(String(255), index=True)
    persist_code = Column(String(255))
    reset_password_code = Column(String(255), index=True)
    permissions = Column(Text)
    activated_at = Column(TIMESTAMP(precision=0), server_default=func.now())
    last_login = Column(TIMESTAMP(precision=0))
    is_activated = Column(Boolean, nullable=False, server_default=text("false"))
    is_guest = Column(Boolean, nullable=False, server_default=text("false"))
    is_superuser = Column(Boolean, nullable=False, server_default=text("false"))
    last_activity = Column(TIMESTAMP(precision=0))
    last_seen = Column(TIMESTAMP(precision=0))
    created_ip_address = Column(String(255))
    last_ip_address = Column(String(255))
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    roles = relationship(Rol, secondary=user_rol_table)
    permisos = relationship(Permiso, secondary=user_permiso_table)
