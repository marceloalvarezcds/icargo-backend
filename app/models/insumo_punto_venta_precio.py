from sqlalchemy import (  # type: ignore
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .insumo_punto_venta import InsumoPuntoVenta


class InsumoPuntoVentaPrecio(AuditMixin, Base):
    """
    Defines the insumo - punto venta - price histoy model
    """

    __table_args__ = (
        UniqueConstraint(
            "insumo_punto_venta_id",
            "precio",
        ),
    )
    id = Column(Integer, primary_key=True)
    insumo_punto_venta_id = Column(Integer, ForeignKey("insumo_punto_venta.id"))
    insumo_punto_venta = relationship(
        InsumoPuntoVenta, uselist=False, back_populates="precios"
    )
    precio = Column(Numeric(38, 10))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    estado = Column(String(15), server_default=EstadoEnum.ACTIVO.value)

    @hybrid_property
    def ciudad_nombre(self):
        return self.insumo_punto_venta.ciudad_nombre

    @hybrid_property
    def gestor_carga_id(self):
        return self.insumo_punto_venta.gestor_carga_id

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.insumo_punto_venta.gestor_carga_nombre

    @hybrid_property
    def insumo_id(self):
        return self.insumo_punto_venta.insumo_id

    @hybrid_property
    def insumo_descripcion(self):
        return self.insumo_punto_venta.insumo_descripcion

    @hybrid_property
    def insumo_moneda_id(self):
        return self.insumo_punto_venta.moneda_id

    @hybrid_property
    def insumo_moneda_nombre(self):
        return self.insumo_punto_venta.moneda_nombre

    @hybrid_property
    def insumo_moneda_simbolo(self):
        return self.insumo_punto_venta.moneda_simbolo

    @hybrid_property
    def insumo_tipo_id(self):
        return self.insumo_punto_venta.insumo_tipo_id

    @hybrid_property
    def insumo_tipo_descripcion(self):
        return self.insumo_punto_venta.insumo_tipo_descripcion

    @hybrid_property
    def insumo_unidad_abreviatura(self):
        return self.insumo_punto_venta.insumo_unidad_abreviatura

    @hybrid_property
    def insumo_unidad_descripcion(self):
        return self.insumo_punto_venta.insumo_unidad_descripcion

    @hybrid_property
    def localidad_nombre(self):
        return self.insumo_punto_venta.localidad_nombre

    @hybrid_property
    def pais_nombre(self):
        return self.insumo_punto_venta.pais_nombre

    @hybrid_property
    def pais_nombre_corto(self):
        return self.insumo_punto_venta.pais_nombre_corto

    @hybrid_property
    def proveedor_id(self):
        return self.insumo_punto_venta.proveedor_id

    @hybrid_property
    def proveedor_nombre(self):
        return self.insumo_punto_venta.proveedor_nombre

    @hybrid_property
    def punto_venta_id(self):
        return self.insumo_punto_venta.punto_venta_id

    @hybrid_property
    def punto_venta_nombre(self):
        return self.insumo_punto_venta.punto_venta_nombre

    @hybrid_property
    def punto_venta_direccion(self):
        return self.insumo_punto_venta.punto_venta_direccion

    @hybrid_property
    def punto_venta_logo(self):
        return self.insumo_punto_venta.punto_venta_logo

    @hybrid_property
    def punto_venta_latitud(self):
        return self.insumo_punto_venta.punto_venta_latitud

    @hybrid_property
    def punto_venta_longitud(self):
        return self.insumo_punto_venta.punto_venta_longitud
