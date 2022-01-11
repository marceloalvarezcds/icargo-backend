from decimal import Decimal
from typing import List

from sqlalchemy import (  # type: ignore
    Boolean,
    Column,
    DateTime,
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
    # Historial de estados
    fecha_aceptado = Column(DateTime)
    fecha_cancelado = Column(DateTime)
    fecha_conciliado = Column(DateTime)
    fecha_contabilizado = Column(DateTime)
    fecha_en_proceso = Column(DateTime)  # <- Misma fecha que estado ARRIBADO_A_CARGA
    fecha_finalizado = Column(DateTime)
    fecha_liquidado = Column(DateTime)
    fecha_nuevo = Column(DateTime)
    fecha_pendiente = Column(DateTime)
    # Historial de estados de OC
    fecha_arribado_a_cargar = Column(DateTime)
    fecha_arribado_a_descargar = Column(DateTime)
    fecha_cargado = Column(DateTime)
    fecha_descargado = Column(DateTime)
    # Relaciones Listas
    anticipos = relationship("OrdenCargaAnticipoRetirado", back_populates="orden_carga")
    complementos = relationship("OrdenCargaComplemento", back_populates="orden_carga")
    descuentos = relationship("OrdenCargaDescuento", back_populates="orden_carga")
    saldos = relationship(
        "OrdenCargaAnticipoSaldo", uselist=False, back_populates="orden_carga"
    )
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
    def estado_valor(self):
        if self.estado == EstadoEnum.EN_PROCESO.value:
            return self.orden_carga_estado
        return self.estado

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
    def flete_origen_nombre(self):
        return self.flete.origen_nombre

    @hybrid_property
    def flete_producto_descripcion(self):
        return self.flete.producto_descripcion

    @hybrid_property
    def flete_remitente_nombre(self):
        return self.flete.remitente_nombre

    @hybrid_property
    def flete_remitente_numero_documento(self):
        return self.flete.remitente.numero_documento

    @hybrid_property
    def flete_tipo(self):
        return self.flete.tipo_flete

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.gestor_carga.nombre

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

    def get_remision_cantidad_total(
        self,
        remisiones: List[OrdenCargaRemisionMixin],
    ) -> Decimal:
        total = Decimal(0)
        for remision in remisiones:
            total += remision.cantidad
        return total
