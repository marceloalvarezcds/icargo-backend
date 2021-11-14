from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import Table  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .permiso import Permiso

rol_permiso_table = Table(
    "rol_permiso",
    Base.metadata,
    Column("rol_id", ForeignKey("rol.id")),
    Column("permiso_id", ForeignKey("permiso.id")),
)


class Rol(AuditMixin, Base):
    """
    Defines the rol model
    """

    id = Column(Integer, primary_key=True)
    codigo = Column(String(255), unique=True)
    descripcion = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    permisos = relationship(Permiso, secondary=rol_permiso_table)
