from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .gestor_carga import GestorCarga
from .insumo import Insumo
from .moneda import Moneda
from .punto_venta import PuntoVenta


class InsumoPuntoVenta(AuditMixin, Base):
    """
    Defines the insumo - punto venta model
    """

    __table_args__ = (
        UniqueConstraint(
            "insumo_id",
            "punto_venta_id",
            "gestor_carga_id",
            "moneda_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    insumo_id = Column(Integer, ForeignKey("insumo.id"))
    insumo = relationship(Insumo, uselist=False, back_populates="punto_ventas")
    punto_venta_id = Column(Integer, ForeignKey("punto_venta.id"))
    punto_venta = relationship(PuntoVenta, uselist=False, back_populates="insumos")
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    estado = Column(String(15), server_default=EstadoEnum.ACTIVO.value)
    precios = relationship(
        "InsumoPuntoVentaPrecio", back_populates="insumo_punto_venta"
    )

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.gestor_carga.nombre

    @hybrid_property
    def insumo_descripcion(self):
        return self.insumo.descripcion

    @hybrid_property
    def insumo_tipo_descripcion(self):
        return self.insumo.tipo_descripcion

    @hybrid_property
    def insumo_unidad_abreviatura(self):
        return self.insumo.unidad_abreviatura

    @hybrid_property
    def insumo_unidad_descripcion(self):
        return self.insumo.unidad_descripcion

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def punto_venta_nombre(self):
        return self.punto_venta.nombre
