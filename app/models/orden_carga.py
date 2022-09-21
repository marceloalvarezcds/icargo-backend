from decimal import Decimal
from typing import List, Optional, Union

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
    OrdenCargaRemisionDestino,
    OrdenCargaRemisionOrigen,
)
from app.utils import number_format

from .camion import Camion
from .centro_operativo import CentroOperativo
from .flete import Flete
from .gestor_carga import GestorCarga
from .moneda import Moneda
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
    modify_by_movimiento = Column(Boolean, server_default=text("false"))
    # FIN Tramo de OC
    # INICIO Cantidad y Flete
    # inicio - Condiciones para el Gestor de Carga
    condicion_gestor_carga_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    condicion_gestor_carga_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[condicion_gestor_carga_moneda_id]
    )
    condicion_gestor_carga_tarifa = Column(Numeric(38, 10))
    # fin - Condiciones para el Gestor de Carga
    # inicio - Condiciones para el Propietario
    condicion_propietario_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    condicion_propietario_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[condicion_propietario_moneda_id]
    )
    condicion_propietario_tarifa = Column(Numeric(38, 10))
    # fin - Condiciones para el Propietario
    # FIN Cantidad y Flete
    # INICIO Mermas de Fletes
    # inicio - Mermas para el Gestor de Carga
    merma_gestor_carga_valor = Column(Numeric(38, 10))
    merma_gestor_carga_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    merma_gestor_carga_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[merma_gestor_carga_moneda_id]
    )
    merma_gestor_carga_es_porcentual = Column(Boolean, server_default=text("false"))
    merma_gestor_carga_tolerancia = Column(Numeric(38, 10))
    # fin - Mermas para el Gestor de Carga
    # inicio - Mermas para el Propietario
    merma_propietario_valor = Column(Numeric(38, 10))
    merma_propietario_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    merma_propietario_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[merma_propietario_moneda_id]
    )
    merma_propietario_es_porcentual = Column(Boolean, server_default=text("false"))
    merma_propietario_tolerancia = Column(Numeric(38, 10))
    # fin - Mermas para el Propietario
    # FIN Mermas de Fletes
    # Relaciones Listas
    historial = relationship("OrdenCargaEstadoHistorial", back_populates="orden_carga")
    anticipos = relationship("OrdenCargaAnticipoRetirado", back_populates="orden_carga")
    movimientos = relationship("Movimiento", back_populates="orden_carga")
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
        return "Liberados" if self.anticipos_liberados else "Bloqueados"

    @hybrid_property
    def camion_chofer_nombre(self):
        return self.camion.chofer_nombre

    @hybrid_property
    def camion_chofer_numero_documento(self):
        return self.camion.chofer_numero_documento

    @hybrid_property
    def camion_chofer_puede_recibir_anticipos(self):
        return self.camion.chofer_puede_recibir_anticipos

    @hybrid_property
    def camion_limite_cantidad_oc_activas(self):
        return self.camion.limite_cantidad_oc_activas

    @hybrid_property
    def camion_limite_monto_anticipos(self):
        return (
            self.camion.limite_monto_anticipos
            if self.camion.limite_monto_anticipos
            else Decimal(0)
        )

    @hybrid_property
    def camion_monto_anticipo_disponible(self):
        return (
            self.camion.monto_anticipo_disponible
            if self.camion.monto_anticipo_disponible
            else Decimal(0)
        )

    @hybrid_property
    def camion_total_anticipos_retirados_en_estado_pendiente_o_en_proceso(self):
        return self.camion.total_anticipos_retirados_en_estado_pendiente_o_en_proceso

    @hybrid_property
    def camion_placa(self):
        return self.camion.placa

    @hybrid_property
    def camion_propietario_nombre(self):
        return self.camion.propietario_nombre

    @hybrid_property
    def camion_propietario_puede_recibir_anticipos(self):
        return self.camion.propietario_puede_recibir_anticipos

    @hybrid_property
    def cantidad_destino(self):
        return self.get_remision_cantidad_total_kg(self.remisiones_destino)

    @hybrid_property
    def cantidad_origen(self):
        return self.get_remision_cantidad_total_kg(self.remisiones_origen)

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
    def fecha_conciliacion(self):
        item = self.get_estado_in_historial(EstadoEnum.CONCILIADO)
        return item.created_at if item else None

    @hybrid_property
    def total_anticipo_complemento(self):
        return sum(x.propietario_monto for x in self.complementos if x.anticipado)

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
    def flete_gestor_carga_detalle(self):
        remi = f"{self.flete.remitente_nombre} ||"
        dest = f"P.Dest.: {number_format(self.cantidad_destino)}Kg ||"
        tari = f"{number_format(self.flete_tarifa_gestor_carga)}{self.flete_tarifa_unidad_gestor_carga} ||"  # noqa: B950
        nums = f"Nº Rem: {self.remisiones} || Tickets: {self.nro_tickets} ||"
        ubic = f"Ori: {self.origen_nombre} || Des: {self.destino_nombre}"
        return f"{remi} {dest} {tari} {nums} {ubic}"

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
    def flete_monto_efectivo_complemento(self):
        return self.total_anticipo_complemento + self.flete_monto_efectivo

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
    def flete_propietario_detalle(self):
        remi = f"{self.flete.remitente_nombre} ||"
        dest = f"P.Dest.: {number_format(self.cantidad_destino)}Kg ||"
        tari = f"{number_format(self.flete_tarifa)}{self.flete_tarifa_unidad} ||"
        nums = f"Nº Rem: {self.remisiones} || Tickets: {self.nro_tickets} ||"
        ubic = f"Ori: {self.origen_nombre} || Des: {self.destino_nombre}"
        return f"{remi} {dest} {tari} {nums} {ubic}"

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
    def flete_tarifa_gestor_carga(self):
        return self.flete.condicion_gestor_carga_tarifa

    @hybrid_property
    def flete_tarifa_unidad(self):
        return f"{self.flete.condicion_propietario_moneda.simbolo}/{self.flete.condicion_propietario_unidad.abreviatura}"  # noqa

    @hybrid_property
    def flete_tarifa_unidad_gestor_carga(self):
        return f"{self.flete.condicion_gestor_carga_moneda.simbolo}/{self.flete.condicion_gestor_carga_unidad.abreviatura}"  # noqa

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
    def gestor_carga_moneda_simbolo(self):
        return self.gestor_carga.moneda_simbolo

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
    def merma_gestor_carga_detalle(self):
        remi = f"{self.flete.remitente_nombre} ||"
        diff = f"Dif.: {number_format(self.diferencia_origen_destino)}Kg ||"
        totl = f"Tol.: {number_format(self.resultado_gestor_carga_tolerancia_kg)}Kg ||"
        merm = f"M.: {number_format(self.resultado_gestor_carga_merma)}Kg ||"
        mval = f"{number_format(self.merma_gestor_carga_valor)}Grs/Kg ||"
        nums = f"Nº Rem: {self.remisiones} || Tickets: {self.nro_tickets} ||"
        ubic = f"Ori: {self.origen_nombre} || Des: {self.destino_nombre}"
        return f"{remi} {diff} {totl} {merm} {mval} {nums} {ubic}"

    @hybrid_property
    def merma_gestor_carga_es_porcentual_descripcion(self):
        return "Si" if self.merma_gestor_carga_es_porcentual else "No"

    @hybrid_property
    def merma_gestor_carga_tolerancia_kg(self):
        return (
            self.merma_gestor_carga_tolerancia
            if self.merma_gestor_carga_es_porcentual
            else self.merma_gestor_carga_tolerancia
            * self.flete.merma_gestor_carga_unidad.conversion_kg
        )

    @hybrid_property
    def merma_propietario_detalle(self):
        remi = f"{self.flete.remitente_nombre} ||"
        diff = f"Dif.: {number_format(self.diferencia_origen_destino)}Kg ||"
        totl = f"Tol.: {number_format(self.resultado_propietario_tolerancia_kg)}Kg ||"
        merm = f"M.: {number_format(self.resultado_propietario_merma)}Kg ||"
        mval = f"{number_format(self.merma_propietario_valor)}Grs/Kg ||"
        nums = f"Nº Rem: {self.remisiones} || Tickets: {self.nro_tickets} ||"
        ubic = f"Ori: {self.origen_nombre} || Des: {self.destino_nombre}"
        return f"{remi} {diff} {totl} {merm} {mval} {nums} {ubic}"

    @hybrid_property
    def merma_propietario_es_porcentual_descripcion(self):
        return "Si" if self.merma_propietario_es_porcentual else "No"

    @hybrid_property
    def merma_propietario_tolerancia_kg(self):
        return (
            self.merma_propietario_tolerancia
            if self.merma_propietario_es_porcentual
            else self.merma_propietario_tolerancia
            * self.flete.merma_propietario_unidad.conversion_kg
        )

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
    def resultado_gestor_carga_merma_valor_total(self):
        return self.merma_gestor_carga_valor * self.resultado_gestor_carga_merma

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
            self.resultado_gestor_carga_total_flete
            - self.resultado_gestor_carga_merma_valor_total
        )

    @hybrid_property
    def resultado_gestor_carga_saldo_total(self):
        return self.resultado_gestor_carga_saldo + (
            self.resultado_propietario_total_complemento_a_cobrar
            - self.resultado_propietario_total_descuento_a_pagar
        )

    @hybrid_property
    def resultado_gestor_carga_tarifa_flete(self):
        return self.condicion_gestor_carga_tarifa

    @hybrid_property
    def resultado_gestor_carga_tolerancia_kg(self):
        return (
            (self.merma_gestor_carga_tolerancia / 100) * self.cantidad_origen
            if self.merma_gestor_carga_es_porcentual
            else self.merma_gestor_carga_tolerancia_kg
        )

    @hybrid_property
    def resultado_gestor_carga_total_flete(self):
        return self.resultado_gestor_carga_tarifa_flete * self.cantidad_destino

    # fin - gestor carga

    # inicio - propietario

    @hybrid_property
    def resultado_propietario_merma_valor_total(self):
        return self.merma_propietario_valor * self.resultado_propietario_merma

    @hybrid_property
    def resultado_propietario_merma_valor_total_moneda_local(self):
        return self.resultado_propietario_merma_valor_total

    @hybrid_property
    def resultado_propietario_merma(self):
        merma = (
            self.diferencia_origen_destino - self.resultado_propietario_tolerancia_kg
        )
        return merma if merma > 0 else 0

    @hybrid_property
    def resultado_propietario_saldo(self):
        return (
            (
                self.resultado_propietario_total_flete
                - self.resultado_propietario_merma_valor_total
            )
            + (
                self.resultado_propietario_total_complemento
                - self.resultado_propietario_total_descuento
            )
            - self.resultado_propietario_total_anticipos_retirados
        )

    @hybrid_property
    def resultado_propietario_saldo_total(self):
        return (
            self.resultado_propietario_saldo
            + self.resultado_propietario_total_anticipos_retirados
        )

    @hybrid_property
    def resultado_propietario_tarifa_flete(self):
        return self.condicion_propietario_tarifa

    @hybrid_property
    def resultado_propietario_tolerancia_kg(self):
        return (
            (self.merma_propietario_tolerancia / 100) * self.cantidad_origen
            if self.merma_propietario_es_porcentual
            else self.merma_propietario_tolerancia_kg
        )

    @hybrid_property
    def resultado_propietario_total_anticipos_retirados(self):
        lista: List[OrdenCargaAnticipoRetirado] = self.anticipos
        return sum(x.monto_retirado for x in lista)

    @hybrid_property
    def resultado_propietario_total_complemento(self):
        lista: List[OrdenCargaComplemento] = self.complementos
        return sum(x.propietario_monto for x in lista)

    @hybrid_property
    def resultado_propietario_total_complemento_a_cobrar(self):
        lista: List[OrdenCargaComplemento] = self.complementos
        return sum(x.remitente_monto for x in lista if x.remitente_monto)

    @hybrid_property
    def resultado_diferencia_complemento(self):
        return (
            self.resultado_propietario_total_complemento_a_cobrar
            - self.resultado_propietario_total_complemento
        )

    @hybrid_property
    def resultado_propietario_total_descuento(self):
        lista: List[OrdenCargaDescuento] = self.descuentos
        return sum(x.propietario_monto for x in lista)

    @hybrid_property
    def resultado_propietario_total_descuento_a_pagar(self):
        lista: List[OrdenCargaDescuento] = self.descuentos
        return sum(x.proveedor_monto for x in lista if x.proveedor_monto)

    @hybrid_property
    def resultado_diferencia_descuento(self):
        return (
            self.resultado_propietario_total_descuento
            - self.resultado_propietario_total_descuento_a_pagar
        )

    @hybrid_property
    def resultado_propietario_total_flete(self):
        return self.resultado_propietario_tarifa_flete * self.cantidad_destino

    # fin - propietario

    # FIN RESULTADO

    # INICIO RESULTADO FLETE

    # inicio - gestor carga

    @hybrid_property
    def resultado_flete_gestor_carga_merma_tolerancia(self):
        return self.flete.merma_gestor_carga_tolerancia

    @hybrid_property
    def resultado_flete_gestor_carga_merma_valor(self):
        return self.flete.merma_gestor_carga_valor

    @hybrid_property
    def resultado_flete_gestor_carga_merma_valor_total(self):
        return (
            self.resultado_flete_gestor_carga_merma_valor
            * self.resultado_flete_gestor_carga_merma
        )

    @hybrid_property
    def resultado_flete_gestor_carga_merma_valor_total_moneda_local(self):
        return self.resultado_flete_gestor_carga_merma_valor_total

    @hybrid_property
    def resultado_flete_gestor_carga_merma(self):
        return (
            (
                self.diferencia_origen_destino
                - self.resultado_flete_gestor_carga_tolerancia_kg
            )
            if (
                self.diferencia_origen_destino
                - self.resultado_flete_gestor_carga_tolerancia_kg
            )
            > 0
            else 0
        )

    @hybrid_property
    def resultado_flete_gestor_carga_saldo(self):
        return (
            self.resultado_flete_gestor_carga_total_flete
            - self.resultado_flete_gestor_carga_merma_valor_total
        )

    @hybrid_property
    def resultado_flete_gestor_carga_saldo_total(self):
        return self.resultado_flete_gestor_carga_saldo + (
            self.resultado_propietario_total_complemento_a_cobrar
            - self.resultado_propietario_total_descuento_a_pagar
        )

    @hybrid_property
    def resultado_flete_gestor_carga_tarifa_flete(self):
        return self.flete.condicion_gestor_carga_tarifa

    @hybrid_property
    def resultado_flete_gestor_carga_tolerancia_kg(self):
        return (
            (self.resultado_flete_gestor_carga_merma_tolerancia / 100)
            * self.cantidad_origen
            if self.flete.merma_gestor_carga_es_porcentual
            else self.flete.merma_gestor_carga_tolerancia_kg
        )

    @hybrid_property
    def resultado_flete_gestor_carga_total_flete(self):
        return self.resultado_flete_gestor_carga_tarifa_flete * self.cantidad_destino

    # fin - gestor carga

    # inicio - propietario

    @hybrid_property
    def resultado_flete_propietario_merma_tolerancia(self):
        return self.flete.merma_propietario_tolerancia

    @hybrid_property
    def resultado_flete_propietario_merma_valor(self):
        return self.flete.merma_propietario_valor

    @hybrid_property
    def resultado_flete_propietario_merma_valor_total(self):
        return (
            self.resultado_flete_propietario_merma_valor
            * self.resultado_flete_propietario_merma
        )

    @hybrid_property
    def resultado_flete_propietario_merma_valor_total_moneda_local(self):
        return self.resultado_flete_propietario_merma_valor_total

    @hybrid_property
    def resultado_flete_propietario_merma(self):
        merma = (
            self.diferencia_origen_destino
            - self.resultado_flete_propietario_tolerancia_kg
        )
        return merma if merma > 0 else 0

    @hybrid_property
    def resultado_flete_propietario_saldo(self):
        return (
            (
                self.resultado_flete_propietario_total_flete
                - self.resultado_flete_propietario_merma_valor_total
            )
            + (
                self.resultado_propietario_total_complemento
                - self.resultado_propietario_total_descuento
            )
            - self.resultado_propietario_total_anticipos_retirados
        )

    @hybrid_property
    def resultado_flete_propietario_saldo_total(self):
        return (
            self.resultado_flete_propietario_saldo
            + self.resultado_propietario_total_anticipos_retirados
        )

    @hybrid_property
    def resultado_flete_propietario_tarifa_flete(self):
        return self.flete.condicion_propietario_tarifa

    @hybrid_property
    def resultado_flete_propietario_tolerancia_kg(self):
        return (
            (self.resultado_flete_propietario_merma_tolerancia / 100)
            * self.cantidad_origen
            if self.flete.merma_propietario_es_porcentual
            else self.flete.merma_propietario_tolerancia_kg
        )

    @hybrid_property
    def resultado_flete_propietario_total_flete(self):
        return self.resultado_flete_propietario_tarifa_flete * self.cantidad_destino

    # fin - propietario

    # FIN RESULTADO FLETE

    @hybrid_property
    def total_anticipo(self):
        return self.flete_limite_credito + self.total_anticipo_complemento

    @hybrid_property
    def total_anticipo_retirado(self):
        return sum(x.total_retirado for x in self.saldos)

    @hybrid_property
    def total_anticipo_disponible(self):
        return self.total_anticipo - self.total_anticipo_retirado

    def get_remision_cantidad_total_kg(
        self,
        remisiones: List[Union[OrdenCargaRemisionDestino, OrdenCargaRemisionOrigen]],
    ) -> Decimal:
        total = Decimal(0)
        for remision in remisiones:
            total += remision.cantidad_kg
        return total

    def get_estado_in_historial(
        self, estado: EstadoEnum
    ) -> Optional[OrdenCargaEstadoHistorial]:
        lista: List[OrdenCargaEstadoHistorial] = self.historial
        for x in lista:
            if x.estado == estado.value:
                return x
        return None

    def find_estado_in_historial(self, estado: EstadoEnum) -> bool:
        return self.get_estado_in_historial(estado) is not None
