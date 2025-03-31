from unicodedata import numeric
from sqlalchemy import (  # type: ignore
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    DateTime,
)

from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum
from app.models.gestor_carga import GestorCarga


class MonedaCotizacion(AuditMixin, Base):
    __tablename__ = "moneda_cotizacion"
    __table_args__ = (
        UniqueConstraint("gestor_carga_id", "moneda_origen_id", "moneda_destino_id"),
    )

    id = Column(Integer, primary_key=True)
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)

    moneda_origen_id = Column(Integer, ForeignKey("moneda.id"))
    moneda_destino_id = Column(Integer, ForeignKey("moneda.id"))

    # 🔹 Relación correcta, separando origen y destino
    moneda_origen = relationship("Moneda", foreign_keys=[moneda_origen_id])
    moneda_destino = relationship("Moneda", foreign_keys=[moneda_destino_id])

    fecha = Column(DateTime)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    cotizacion_moneda = Column(Numeric(38, 10))
