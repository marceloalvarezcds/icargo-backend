from typing import List
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
from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.utils import number_format
from .flete_anticipo import FleteAnticipo
from .insumo_punto_venta_precio import InsumoPuntoVentaPrecio
from .moneda import Moneda
from .orden_carga import OrdenCarga
from .orden_carga_anticipo_porcentaje import OrdenCargaAnticipoPorcentaje
from .punto_venta import PuntoVenta
from .tipo_comprobante import TipoComprobante
from .unidad import Unidad


class OrdenCargaAnticipoRetirado(AuditMixin, Base):
    """
    Defines the orden carga - anticipo retirado model
    """

    id = Column(Integer, primary_key=True)
    flete_anticipo_id = Column(Integer, ForeignKey("flete_anticipo.id"))
    flete_anticipo = relationship(
        FleteAnticipo, uselist=False, back_populates="anticipos"
    )
    orden_carga_id = Column(Integer, ForeignKey("orden_carga.id"))
    orden_carga = relationship(OrdenCarga, uselist=False, back_populates="anticipos")
    orden_carga_anticipo_porcentaje_id = Column(
        Integer, ForeignKey("orden_carga_anticipo_porcentaje.id")
    )
    orden_carga_anticipo_porcentaje = relationship(
        OrdenCargaAnticipoPorcentaje, uselist=False, back_populates="anticipos"
    )
    punto_venta_id = Column(Integer, ForeignKey("punto_venta.id"))
    punto_venta = relationship(PuntoVenta, uselist=False)
    tipo_comprobante_id = Column(Integer, ForeignKey("tipo_comprobante.id"))
    tipo_comprobante = relationship(TipoComprobante, uselist=False)
    numero_comprobante = Column(String(255))
    moneda_id = Column(Integer, ForeignKey("moneda.id"))
    moneda = relationship(Moneda, uselist=False)
    monto_retirado = Column(Numeric(38, 10))
    monto_mon_local = Column(Numeric(38, 10))
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
    movimientos = relationship("Movimiento", back_populates="anticipo")

    @hybrid_property
    def concepto(self):
        return self.flete_anticipo.concepto

    @hybrid_property
    def concepto_detalle(self):
        if self.flete_anticipo.concepto != "EFECTIVO":
            return self.insumo_descripcion
        return self.flete_anticipo.concepto

    @hybrid_property
    def detalle(self):
        producto_info = ""
        if self.insumo_punto_venta_precio:
            producto_info = f" || Precio: {number_format(self.precio_unitario)} || Prod: {self.insumo_descripcion}"  # noqa: B950
            moneda = self.gestor_carga_moneda_simbolo
        else:
            moneda = self.moneda_simbolo

        concepto = f"{self.concepto}: {number_format(self.monto_retirado)}{moneda}"
        punto_venta_producto = f"{producto_info} || {self.punto_venta_nombre}"
        return f"{concepto} {punto_venta_producto}"


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
    def gestor_carga_moneda_simbolo(self):
        return self.orden_carga.gestor_carga_moneda_simbolo

    @hybrid_property
    def insumo_id(self):
        return (
            self.insumo_punto_venta_precio.insumo_id
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_descripcion(self):
        return (
            self.insumo_punto_venta_precio.insumo_descripcion
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_fecha_precio(self):
        return (
            self.insumo_punto_venta_precio.fecha_precio
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_moneda_nombre(self):
        return (
            self.insumo_punto_venta_precio.moneda_nombre
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_moneda_id(self):
        return (
            self.insumo_punto_venta_precio.moneda_id
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_precio(self):
        return (
            self.insumo_punto_venta_precio.precio
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_tipo_descripcion(self):
        return (
            self.insumo_punto_venta_precio.insumo_tipo_descripcion
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_unidad_abreviatura(self):
        return (
            self.insumo_punto_venta_precio.insumo_unidad_abreviatura
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def insumo_unidad_descripcion(self):
        return (
            self.insumo_punto_venta_precio.insumo_unidad_descripcion
            if self.insumo_punto_venta_precio
            else None
        )

    @hybrid_property
    def es_punto_venta(self):
        return (
            self.punto_venta_id is not None
        )

    @hybrid_property
    def moneda_nombre(self):
        return self.moneda.nombre

    @hybrid_property
    def moneda_simbolo(self):
        return self.moneda.simbolo

    @hybrid_property
    def proveedor_id(self):
        return self.punto_venta.proveedor_id

    @hybrid_property
    def proveedor_nombre(self):
        return self.punto_venta.proveedor_nombre

    @hybrid_property
    def punto_venta_nombre(self):
        return self.punto_venta.nombre

    @hybrid_property
    def punto_venta_alias(self):
        return self.punto_venta.nombre_corto

    @hybrid_property
    def punto_venta_documento(self):
        return self.punto_venta.numero_documento

    @hybrid_property
    def punto_venta_pais_nombre(self):
        return self.punto_venta.pais_nombre

    @hybrid_property
    def tipo_anticipo_id(self):
        return self.flete_anticipo.tipo_id

    @hybrid_property
    def tipo_anticipo_descripcion(self):
        return self.flete_anticipo.tipo_descripcion

    @hybrid_property
    def tipo_comprobante_descripcion(self):
        return self.tipo_comprobante.descripcion if self.tipo_comprobante else None

    @hybrid_property
    def tipo_insumo_id(self):
        return self.flete_anticipo.tipo_insumo_id

    @hybrid_property
    def tipo_insumo_descripcion(self):
        return self.flete_anticipo.tipo_insumo_descripcion

    @hybrid_property
    def unidad_abreviatura(self):
        return self.unidad.abreviatura if self.unidad else None

    @hybrid_property
    def unidad_descripcion(self):
        return self.unidad.descripcion if self.unidad else None


    @hybrid_property
    def estado_movimiento_propietario(self):
        movimiento_propietario = next((x for x in self.movimientos if x.propietario_id != None), None)
        return movimiento_propietario.estado if movimiento_propietario else None

    @hybrid_property
    def estado_movimiento_remitente(self):
        movimiento_remitente = next((x for x in self.movimientos if x.remitente_id != None), None)
        return movimiento_remitente.estado if movimiento_remitente else None

    @hybrid_property
    def monto_litro(self):
        if self.cantidad_retirada and self.precio_unitario:
            return self.cantidad_retirada * self.precio_unitario
        return 0

    @hybrid_property
    def estado_movimiento(self):
        if self.movimientos:
            return self.movimientos[0].estado
        return None

    @hybrid_property
    def camion_placa(self):
        return self.orden_carga.camion_placa

    @hybrid_property
    def chofer_nombre(self):
        return self.orden_carga.chofer_nombre
