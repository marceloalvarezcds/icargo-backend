from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .gestor_carga import GestorCarga
from .punto_venta import PuntoVenta


class GestorCargaPuntoVenta(AuditMixin, Base):
    """
    Defines the gestor carga - punto_venta model
    """

    __table_args__ = (
        UniqueConstraint(
            "punto_venta_id",
            "gestor_carga_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    punto_venta_id = Column(Integer, ForeignKey("punto_venta.id"))
    punto_venta = relationship(PuntoVenta, uselist=False, back_populates="gestores")
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    alias = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
