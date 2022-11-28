from decimal import Decimal
from typing import Any, List, Optional

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum

from .flete_anticipo import FleteAnticipo
from .orden_carga import OrdenCarga
from .tipo_anticipo import TipoAnticipo
from .tipo_insumo import TipoInsumo


class OrdenCargaAnticipoPorcentaje(AuditMixin, Base):
    """
    Defines the flete - anticipo model
    """

    __table_args__ = (UniqueConstraint("flete_anticipo_id", "orden_carga_id"),)
    id: int = Column(Integer, primary_key=True)
    porcentaje: Decimal = Column(Numeric(38, 10))
    porcentaje_minimo: Decimal = Column(Numeric(38, 10))
    flete_anticipo_id: int = Column(Integer, ForeignKey("flete_anticipo.id"))
    flete_anticipo: FleteAnticipo = relationship(FleteAnticipo, uselist=False)
    orden_carga_id: int = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga: OrdenCarga = relationship(
        OrdenCarga, uselist=False, back_populates="porcentaje_anticipos"
    )
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    anticipos: List[Any] = relationship(
        "OrdenCargaAnticipoRetirado", back_populates="orden_carga_anticipo_porcentaje"
    )
    saldos: List[Any] = relationship(
        "OrdenCargaAnticipoSaldo", back_populates="orden_carga_anticipo_porcentaje"
    )

    @hybrid_property
    def concepto(self) -> str:
        return (
            self.tipo_insumo_descripcion if self.tipo_insumo else self.tipo_descripcion
        )

    @hybrid_property
    def flete_id(self) -> int:
        return self.flete_anticipo.flete_id

    @hybrid_property
    def tipo_id(self) -> int:
        return self.flete_anticipo.tipo_id

    @hybrid_property
    def tipo(self) -> TipoAnticipo:
        return self.flete_anticipo.tipo

    @hybrid_property
    def tipo_descripcion(self) -> str:
        return self.tipo.descripcion

    @hybrid_property
    def tipo_insumo_id(self) -> int:
        return self.flete_anticipo.tipo_insumo_id

    @hybrid_property
    def tipo_insumo(self) -> Optional[TipoInsumo]:
        return self.flete_anticipo.tipo_insumo

    @hybrid_property
    def tipo_insumo_descripcion(self) -> Optional[str]:
        return self.tipo_insumo.descripcion if self.tipo_insumo else None
