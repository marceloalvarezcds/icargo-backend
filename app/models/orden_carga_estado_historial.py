from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum

from .orden_carga import OrdenCarga


class OrdenCargaEstadoHistorial(AuditMixin, Base):
    """
    Defines the orden carga - estado historial model
    """

    __table_args__ = (
        UniqueConstraint(
            "orden_carga_id",
            "estado",
        ),
    )
    id = Column(Integer, primary_key=True)
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(OrdenCarga, uselist=False, back_populates="historial")
    estado = Column(String(15), server_default=EstadoEnum.NUEVO.value)
