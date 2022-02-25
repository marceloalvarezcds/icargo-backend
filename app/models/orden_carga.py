from decimal import Decimal
from typing import List

from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum
from app.schemas import (
    OrdenCargaAnticipoRetirado,
    OrdenCargaComplemento,
    OrdenCargaDescuento,
    OrdenCargaEstadoHistorial,
)

from .camion import Camion
from .centro_operativo import CentroOperativo
from .flete import Flete
from .gestor_carga import GestorCarga
from .orden_carga_remision_mixin import OrdenCargaRemisionMixin
from .semi import Semi


class OrdenCarga(AuditMixin, Base):
    id = Column(Integer, primary_key=True)
    camion_id = Column(Integer, ForeignKey("camion.id"))
    camion = relationship(Camion, uselist=False)
    semi_id = Column(Integer, ForeignKey("semi.id"))
    semi = relationship(Semi, uselist=False)
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False)
    cantidad_nominada = Column(Numeric(38, 10))
    comentarios = Column(Text)
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    # Campos para la edición
    estado = Column(String(15), server_default=EstadoEnum.NUEVO.value)
    orden_carga_estado = Column(String(25), server_default=EstadoEnum.PENDIENTE.value)
    anticipos_liberados = Column(Boolean, server_default=text("false"))
    # INICIO Tramo de OC
    origen_id = Column(Integer, ForeignKey("centro_operativo.id"))
    origen = relationship(CentroOperativo, uselist=False, foreign_keys=[origen_id])
    destino_id = Column(Integer, ForeignKey("centro_operativo.id"))
    destino = relationship(CentroOperativo, uselist=False, foreign_keys=[destino_id])
    # FIN Tramo de OC
    # Relaciones Listas
    historial = relationship("OrdenCargaEstadoHistorial", back_populates="orden_carga")
    anticipos = relationship("OrdenCargaAnticipoRetirado", back_populates="orden_carga")
    complementos = relationship("OrdenCargaComplemento", back_populates="orden_carga")
    descuentos = relationship("OrdenCargaDescuento", back_populates="orden_carga")
    saldos = relationship("OrdenCargaAnticipoSaldo", back_populates="orden_carga")
    remisiones_origen = relationship(
        "OrdenCargaRemisionOrigen", back_populates="orden_carga"
    )
    remisiones_destino = relationship(
        "OrdenCargaRemisionDestino", back_populates="orden_carga"
    )

    @hybrid_property
    def anticipos_liberados_descripcion(self):
        return "Si" if self.anticipos_liberados else "No"

    @hybrid_property
    def camion_chofer_nombre(self):
        return self.camion.chofer_nombre

    @hybrid_property
    def camion_chofer_numero_documento(self):
        return self.camion.chofer_numero_documento

    @hybrid_property
    def camion_placa(self):
        return self.camion.placa

    @hybrid_property
    def camion_propietario_nombre(self):
        return self.camion.propietario_nombre

    @hybrid_property
    def cantidad_destino(self):
        return self.get_remision_cantidad_total(self.remisiones_destino)

    @hybrid_property
    def cantidad_origen(self):
        return self.get_remision_cantidad_total(self.remisiones_origen)

    @hybrid_property
    def destino_nombre(self):
        return self.destino.nombre

    @hybrid_property
    def diferencia_origen_destino(self):
        return self.cantidad_origen - self.cantidad_destino

    @hybrid_property
    def estado_valor(self):
        if self.estado == EstadoEnum.EN_PROCESO.value:
            return self.orden_carga_estado
        return self.estado

    @hybrid_property
    def flete_anticipo_maximo(self):
        return self.flete.anticipo_maximo

    @hybrid_property
    def flete_anticipos(self):
        return self.flete.anticipos

    @hybrid_property
    def flete_destino_id(self):
        return self.flete.destino_id

    @hybrid_property
    def flete_destino_nombre(self):
        return self.flete.destino_nombre

    @hybrid_property
    def flete_gestor_carga_id(self):
        return self.flete.gestor_carga_id

    @hybrid_property
    def flete_gestor_carga_nombre(self):
        return self.flete.gestor_carga_nombre

    @hybrid_property
    def flete_limite_credito(self):  # total anticipo
        return (self.flete_anticipo_maximo / Decimal(100)) * self.flete_proyectado

    @hybrid_property
    def flete_numero_lote(self):
        return self.flete.numero_lote

    @hybrid_property
    def flete_monto_efectivo(self):
        return (self.flete.porcentaje_efectivo / Decimal(100)) * self.flete_proyectado

    @hybrid_property
    def flete_origen_id(self):
        return self.flete.origen_id

    @hybrid_property
    def flete_origen_nombre(self):
        return self.flete.origen_nombre

    @hybrid_property
    def flete_producto_descripcion(self):
        return self.flete.producto_descripcion

    @hybrid_property
    def flete_proyectado(self):
        return self.flete_tarifa * self.cantidad_nominada

    @hybrid_property
    def flete_remitente_nombre(self):
        return self.flete.remitente_nombre

    @hybrid_property
    def flete_remitente_numero_documento(self):
        return self.flete.remitente.numero_documento

    @hybrid_property
    def flete_tarifa(self):
        return self.flete.condicion_propietario_tarifa

    @hybrid_property
    def flete_tipo(self):
        return self.flete.tipo_flete

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.gestor_carga.nombre

    @hybrid_property
    def gestor_carga_moneda_nombre(self):
        return self.gestor_carga.moneda_nombre

    @hybrid_property
    def is_aceptado(self):
        return self.find_estado_in_historial(EstadoEnum.ACEPTADO)

    @hybrid_property
    def is_cancelado(self):
        return self.find_estado_in_historial(EstadoEnum.CANCELADO)

    @hybrid_property
    def is_conciliado(self):
        return self.find_estado_in_historial(EstadoEnum.CONCILIADO)

    @hybrid_property
    def is_contabilizado(self):
        return self.find_estado_in_historial(EstadoEnum.CONTABILIZADO)

    @hybrid_property
    def is_en_proceso(self):
        return self.find_estado_in_historial(EstadoEnum.EN_PROCESO)

    @hybrid_property
    def is_finalizado(self):
        return self.find_estado_in_historial(EstadoEnum.FINALIZADO)

    @hybrid_property
    def is_liquidado(self):
        return self.find_estado_in_historial(EstadoEnum.LIQUIDADO)

    @hybrid_property
    def nro_tickets(self):
        return ", ".join([x.numero_documento for x in self.remisiones_destino])

    @hybrid_property
    def origen_nombre(self):
        return self.origen.nombre

    @hybrid_property
    def remisiones(self):
        return ", ".join([x.numero_documento for x in self.remisiones_origen])

    @hybrid_property
    def semi_placa(self):
        return self.semi.placa

    # INICIO RESULTADO

    # inicio - gestor carga

    @hybrid_property
    def resultado_gestor_carga_merma_tolerancia(self):
        return self.flete.merma_gestor_cuenta_tolerancia

    @hybrid_property
    def resultado_gestor_carga_merma_valor(self):
        return self.flete.merma_gestor_cuenta_valor

    @hybrid_property
    def resultado_gestor_carga_merma_valor_total(self):
        return (
            self.resultado_gestor_carga_merma_valor * self.resultado_gestor_carga_merma
        )

    @hybrid_property
    def resultado_gestor_carga_merma_valor_total_moneda_local(self):
        return self.resultado_gestor_carga_merma_valor_total

    @hybrid_property
    def resultado_gestor_carga_merma(self):
        return (
            (self.diferencia_origen_destino - self.resultado_gestor_carga_tolerancia_kg)
            if (
                self.diferencia_origen_destino
                - self.resultado_gestor_carga_tolerancia_kg
            )
            > 0
            else 0
        )

    @hybrid_property
    def resultado_gestor_carga_saldo(self):
        return (
            self.resultado_gestor_carga_merma_valor_total
            - self.resultado_gestor_carga_total_flete
        ) + self.resultado_gestor_carga_merma

    @hybrid_property
    def resultado_gestor_carga_tarifa_flete(self):
        return self.flete.condicion_gestor_cuenta_tarifa

    @hybrid_property
    def resultado_gestor_carga_tolerancia_kg(self):
        return (
            (self.resultado_gestor_carga_merma_tolerancia / 100) * self.cantidad_origen
            if self.flete.merma_gestor_cuenta_es_porcentual
            else self.resultado_gestor_carga_merma_tolerancia
        )

    @hybrid_property
    def resultado_gestor_carga_total_flete(self):
        return self.resultado_gestor_carga_tarifa_flete * self.cantidad_destino

    # fin - gestor carga

    # inicio - propietario

    @hybrid_property
    def resultado_propietario_merma_tolerancia(self):
        return self.flete.merma_propietario_tolerancia

    @hybrid_property
    def resultado_propietario_merma_valor(self):
        return self.flete.merma_propietario_valor

    @hybrid_property
    def resultado_propietario_merma_valor_total(self):
        return self.resultado_propietario_merma_valor * self.resultado_propietario_merma

    @hybrid_property
    def resultado_propietario_merma_valor_total_moneda_local(self):
        return self.resultado_propietario_merma_valor_total

    @hybrid_property
    def resultado_propietario_merma(self):
        return (
            (self.diferencia_origen_destino - self.resultado_propietario_tolerancia_kg)
            if (
                self.diferencia_origen_destino
                - self.resultado_propietario_tolerancia_kg
            )
            > 0
            else 0
        )

    @hybrid_property
    def resultado_propietario_saldo(self):
        return (
            (
                self.resultado_propietario_merma_valor_total
                - self.resultado_gestor_carga_total_flete
            )
            + (
                self.resultado_propietario_total_descuento
                - self.resultado_propietario_total_complemento
            )
            + self.resultado_propietario_merma
        )

    @hybrid_property
    def resultado_propietario_tarifa_flete(self):
        return self.flete.condicion_propietario_tarifa

    @hybrid_property
    def resultado_propietario_tolerancia_kg(self):
        return (
            (self.resultado_propietario_merma_tolerancia / 100) * self.cantidad_origen
            if self.flete.merma_propietario_es_porcentual
            else self.resultado_propietario_merma_tolerancia
        )

    @hybrid_property
    def resultado_propietario_total_anticipos_retirados(self):
        lista: List[OrdenCargaAnticipoRetirado] = self.anticipos
        total = Decimal(0)
        for item in lista:
            total += item.monto_retirado
        return total

    @hybrid_property
    def resultado_propietario_total_complemento(self):
        lista: List[OrdenCargaComplemento] = self.complementos
        total = Decimal(0)
        for item in lista:
            total += item.propietario_monto
        return total

    @hybrid_property
    def resultado_propietario_total_descuento(self):
        lista: List[OrdenCargaDescuento] = self.descuentos
        total = Decimal(0)
        for item in lista:
            total += item.propietario_monto
        return total

    @hybrid_property
    def resultado_propietario_total_flete(self):
        return self.resultado_propietario_tarifa_flete * self.cantidad_destino

    # fin - propietario

    # FIN RESULTADO

    def get_remision_cantidad_total(
        self,
        remisiones: List[OrdenCargaRemisionMixin],
    ) -> Decimal:
        total = Decimal(0)
        for remision in remisiones:
            total += remision.cantidad
        return total

    def find_estado_in_historial(self, estado: EstadoEnum) -> bool:
        lista: List[OrdenCargaEstadoHistorial] = self.historial
        for x in lista:
            if x.estado == estado.value:
                return True
        return False
