from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .centro_operativo import CentroOperativo
from .gestor_carga import GestorCarga


class GestorCargaCentroOperativo(AuditMixin, Base):
    """
    Defines the gestor carga - centro operativo model
    """

    __table_args__ = (
        UniqueConstraint(
            "centro_operativo_id",
            "gestor_carga_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    centro_operativo_id = Column(Integer, ForeignKey("centro_operativo.id"))
    centro_operativo = relationship(CentroOperativo, uselist=False)
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    alias = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
