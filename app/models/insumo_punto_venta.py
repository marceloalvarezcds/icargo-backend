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
    def ciudad_nombre(self):
        return self.punto_venta.ciudad_nombre

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.gestor_carga.nombre

    @hybrid_property
    def insumo_descripcion(self):
        return self.insumo.descripcion

    @hybrid_property
    def insumo_tipo_id(self):
        return self.insumo.tipo_id

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
    def localidad_nombre(self):
        return self.punto_venta.localidad_nombre

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def moneda_simbolo(self):
        return self.moneda.simbolo

    @hybrid_property
    def pais_nombre(self):
        return self.punto_venta.pais_nombre

    @hybrid_property
    def pais_nombre_corto(self):
        return self.punto_venta.pais_nombre_corto

    @hybrid_property
    def proveedor_id(self):
        return self.punto_venta.proveedor_id

    @hybrid_property
    def proveedor_nombre(self):
        return self.punto_venta.proveedor_nombre
    
    @hybrid_property
    def proveedor_documento(self):
        return self.punto_venta.proveedor_documento
    
    @hybrid_property
    def created_insumo(self):
        return self.insumo.fecha_creacion
    
    @hybrid_property
    def marca_insumo(self):
        return self.insumo.marca

    @hybrid_property
    def punto_venta_nombre(self):
        return self.punto_venta.nombre

    @hybrid_property
    def punto_venta_direccion(self):
        return self.punto_venta.direccion

    @hybrid_property
    def punto_venta_logo(self):
        return self.punto_venta.logo

    @hybrid_property
    def punto_venta_latitud(self):
        return self.punto_venta.latitud

    @hybrid_property
    def punto_venta_longitud(self):
        return self.punto_venta.longitud

    @hybrid_property
    def precio(self):
        if self.precios:
            return self.precios[0].precio 
        return None  

    @hybrid_property
    def fecha_inicio(self):
        if self.precios:
            return self.precios[0].fecha_inicio 
        return None  

    @hybrid_property
    def fecha_fin(self):
        if self.precios:
            return self.precios[0].fecha_fin 
        return None  