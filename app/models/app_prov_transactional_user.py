from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .punto_venta import PuntoVenta


class TransactionalUser(AuditMixin, Base):
    """
    Defines the TransactionalUser model
    """

    id: int = Column(Integer, primary_key=True)
    numero_documento: str = Column(String(15))
    nombre: str = Column(String(255))
    apellido: str = Column(String(255))
    telefono: str = Column(String(25))
    pin: str = Column(String(255))
    estado: str = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    punto_venta_id: int = Column(Integer, ForeignKey("punto_venta.id"))
    punto_venta: PuntoVenta = relationship(PuntoVenta, uselist=False)

    @hybrid_property
    def is_activated(self) -> bool:
        return self.estado == EstadoEnum.ACTIVO.value
