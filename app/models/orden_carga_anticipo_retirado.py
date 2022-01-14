from sqlalchemy import (  # type: ignore
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .flete_anticipo import FleteAnticipo
from .insumo_punto_venta_precio import InsumoPuntoVentaPrecio
from .moneda import Moneda
from .orden_carga import OrdenCarga
from .punto_venta import PuntoVenta
from .tipo_comprobante import TipoComprobante
from .unidad import Unidad


class OrdenCargaAnticipoRetirado(AuditMixin, Base):
    """
    Defines the orden carga - anticipo retirado model
    """

    __table_args__ = (
        UniqueConstraint("flete_anticipo_id", "orden_carga_id", "punto_venta_id"),
    )
    id = Column(Integer, primary_key=True)
    flete_anticipo_id = Column(Integer, ForeignKey("flete_anticipo.id"))
    flete_anticipo = relationship(
        FleteAnticipo, uselist=False, back_populates="anticipos"
    )
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(OrdenCarga, uselist=False, back_populates="anticipos")
    punto_venta_id = Column(Integer, ForeignKey("punto_venta.id"))
    punto_venta = relationship(PuntoVenta, uselist=False)
    tipo_comprobante_id = Column(Integer, ForeignKey("tipo_comprobante.id"))
    tipo_comprobante = relationship(TipoComprobante, uselist=False)
    numero_comprobante = Column(String(255))
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    monto_retirado = Column(Numeric(38, 10))
    observacion = Column(Text)
    # OPCIONALES
    insumo_punto_venta_precio_id = Column(
        Integer, ForeignKey("insumo_punto_venta_precio.id")
    )
    insumo_punto_venta_precio = relationship(InsumoPuntoVentaPrecio, uselist=False)
    unidad_id = Column(
        Integer, ForeignKey("unidad.id")
    )  # Por si el usuario necesite cargar cuantos litros de combustible retiró
    unidad = relationship(Unidad, uselist=False)
    cantidad_retirada = Column(Numeric(38, 10))
    precio_unitario = Column(
        Numeric(38, 10)
    )  # No se usa para calcular los movimientos, solo para cargar por el momento

    @hybrid_property
    def gestor_carga_id(self):
        return self.orden_carga.gestor_carga_id

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.orden_carga.gestor_carga_nombre

    @hybrid_property
    def gestor_carga_moneda_nombre(self):
        return self.orden_carga.gestor_carga_moneda_nombre

    @hybrid_property
    def insumo_descripcion(self):
        return self.insumo_punto_venta_precio.insumo_descripcion

    @hybrid_property
    def insumo_fecha_precio(self):
        return self.insumo_punto_venta_precio.fecha_precio

    @hybrid_property
    def insumo_moneda_nombre(self):
        return self.insumo_punto_venta_precio.moneda_nombre

    @hybrid_property
    def insumo_precio(self):
        return self.insumo_punto_venta_precio.precio

    @hybrid_property
    def insumo_tipo_descripcion(self):
        return self.insumo_punto_venta_precio.insumo_tipo_descripcion

    @hybrid_property
    def insumo_unidad_abreviatura(self):
        return self.insumo_punto_venta_precio.insumo_unidad_abreviatura

    @hybrid_property
    def insumo_unidad_descripcion(self):
        return self.insumo_punto_venta_precio.insumo_unidad_descripcion

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def proveedor_nombre(self):
        return self.punto_venta.proveedor_nombre

    @hybrid_property
    def punto_venta_nombre(self):
        return self.punto_venta.nombre

    @hybrid_property
    def punto_venta_pais_nombre(self):
        return self.punto_venta.pais_nombre

    @hybrid_property
    def tipo_anticipo_descripcion(self):
        return self.flete_anticipo.tipo_descripcion

    @hybrid_property
    def tipo_comprobante_descripcion(self):
        return self.tipo_comprobante.descripcion

    @hybrid_property
    def tipo_insumo_descripcion(self):
        return self.flete_anticipo.tipo_insumo_descripcion

    @hybrid_property
    def unidad_abreviatura(self):
        return self.unidad.abreviatura

    @hybrid_property
    def unidad_descripcion(self):
        return self.unidad.descripcion
