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
from sqlalchemy.sql.schema import Table  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums import EstadoEnum, TipoFleteEnum
from app.utils import (
    get_flete_anticipo_efectivo,
    get_porcentaje_maximo_by_flete_anticipo_list,
)

from .centro_operativo import CentroOperativo
from .centro_operativo_contacto_gestor_carga import CentroOperativoContactoGestorCarga
from .gestor_carga import GestorCarga
from .moneda import Moneda
from .producto import Producto
from .remitente import Remitente
from .remitente_contacto_gestor_carga import RemitenteContactoGestorCarga
from .tipo_carga import TipoCarga
from .unidad import Unidad
from .user import User

flete_centro_operativo_contacto_table = Table(
    "flete_centro_operativo_contacto",
    Base.metadata,
    Column("flete_id", ForeignKey("flete.id")),
    Column(
        "centro_operativo_contacto_id",
        ForeignKey("centro_operativo_contacto_gestor_carga.id"),
    ),
)

flete_remitente_contacto_table = Table(
    "flete_remitente_contacto",
    Base.metadata,
    Column("flete_id", ForeignKey("flete.id")),
    Column(
        "remitente_contacto_id",
        ForeignKey("remitente_contacto_gestor_carga.id"),
    ),
)

flete_user_contacto_table = Table(
    "flete_user_contacto",
    Base.metadata,
    Column("flete_id", ForeignKey("flete.id")),
    Column("user_contacto_id", ForeignKey("user.id")),
)


class Flete(AuditMixin, Base):
    """
    Defines the flete model
    """

    id = Column(Integer, primary_key=True)
    remitente_id = Column(Integer, ForeignKey("remitente.id"))
    remitente = relationship(Remitente, uselist=False)
    producto_id = Column(Integer, ForeignKey("producto.id"))
    producto = relationship(Producto, uselist=False)
    tipo_carga_id = Column(Integer, ForeignKey("tipo_carga.id"))
    tipo_carga = relationship(TipoCarga, uselist=False)
    numero_lote = Column(String(255))
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    publicado = Column(Boolean, server_default=text("false"))
    es_subasta = Column(Boolean, server_default=text("false"))
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    saldo = Column(Numeric(38, 10))
    # INICIO Tramo de Fletes
    origen_id = Column(Integer, ForeignKey("centro_operativo.id"))
    origen = relationship(CentroOperativo, uselist=False, foreign_keys=[origen_id])
    origen_indicacion = Column(Text)
    destino_id = Column(Integer, ForeignKey("centro_operativo.id"))
    destino = relationship(CentroOperativo, uselist=False, foreign_keys=[destino_id])
    destino_indicacion = Column(Text)
    distancia = Column(Numeric(38, 10))
    # FIN Tramo de Fletes
    # INICIO Cantidad y Flete
    condicion_cantidad = Column(Numeric(38, 10))
    # inicio - Condiciones para el Gestor de Cuenta
    condicion_gestor_cuenta_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    condicion_gestor_cuenta_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[condicion_gestor_cuenta_moneda_id]
    )
    condicion_gestor_cuenta_tarifa = Column(Numeric(38, 10))
    condicion_gestor_cuenta_unidad_id = Column(Integer, ForeignKey("unidad.id"))
    condicion_gestor_cuenta_unidad = relationship(
        Unidad, uselist=False, foreign_keys=[condicion_gestor_cuenta_unidad_id]
    )
    # fin - Condiciones para el Gestor de Cuenta
    # inicio - Condiciones para el Propietario
    condicion_propietario_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    condicion_propietario_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[condicion_propietario_moneda_id]
    )
    condicion_propietario_tarifa = Column(Numeric(38, 10))
    condicion_propietario_unidad_id = Column(Integer, ForeignKey("unidad.id"))
    condicion_propietario_unidad = relationship(
        Unidad, uselist=False, foreign_keys=[condicion_propietario_unidad_id]
    )
    # fin - Condiciones para el Propietario
    # FIN Cantidad y Flete
    # INICIO Mermas de Fletes
    # inicio - Mermas para el Gestor de Cuenta
    merma_gestor_cuenta_valor = Column(Numeric(38, 10))
    merma_gestor_cuenta_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    merma_gestor_cuenta_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[merma_gestor_cuenta_moneda_id]
    )
    merma_gestor_cuenta_unidad_id = Column(Integer, ForeignKey("unidad.id"))
    merma_gestor_cuenta_unidad = relationship(
        Unidad, uselist=False, foreign_keys=[merma_gestor_cuenta_unidad_id]
    )
    merma_gestor_cuenta_es_porcentual = Column(Boolean, server_default=text("false"))
    merma_gestor_cuenta_tolerancia = Column(Numeric(38, 10))
    # fin - Mermas para el Gestor de Cuenta
    # inicio - Mermas para el Propietario
    merma_propietario_valor = Column(Numeric(38, 10))
    merma_propietario_moneda_id = Column(Integer, ForeignKey("moneda.id"))
    merma_propietario_moneda = relationship(
        Moneda, uselist=False, foreign_keys=[merma_propietario_moneda_id]
    )
    merma_propietario_unidad_id = Column(Integer, ForeignKey("unidad.id"))
    merma_propietario_unidad = relationship(
        Unidad, uselist=False, foreign_keys=[merma_propietario_unidad_id]
    )
    merma_propietario_es_porcentual = Column(Boolean, server_default=text("false"))
    merma_propietario_tolerancia = Column(Numeric(38, 10))
    # fin - Mermas para el Propietario
    # FIN Mermas de Fletes
    vigencia_anticipos = Column(DateTime)
    anticipos = relationship("FleteAnticipo", back_populates="flete")
    complementos = relationship("FleteComplemento", back_populates="flete")
    descuentos = relationship("FleteDescuento", back_populates="flete")
    # INICIO Emisión de Órdenes
    emision_orden_texto_legal = Column(Text)
    emision_orden_detalle = Column(Text)
    emision_orden_centro_operativo_destinatarios = relationship(
        CentroOperativoContactoGestorCarga,
        secondary=flete_centro_operativo_contacto_table,
    )
    emision_orden_remitente_destinatarios = relationship(
        RemitenteContactoGestorCarga,
        secondary=flete_remitente_contacto_table,
    )
    emision_orden_user_destinatarios = relationship(
        User,
        secondary=flete_user_contacto_table,
    )
    # FIN Emisión de Órdenes

    @hybrid_property
    def anticipo_maximo(self):
        return get_porcentaje_maximo_by_flete_anticipo_list(self.anticipos)

    @hybrid_property
    def condicion_gestor_cuenta_moneda_nombre(self):
        return self.condicion_gestor_cuenta_moneda.nombre

    @hybrid_property
    def condicion_gestor_cuenta_unidad_descripcion(self):
        return self.condicion_gestor_cuenta_unidad.descripcion

    @hybrid_property
    def condicion_propietario_moneda_nombre(self):
        return self.condicion_propietario_moneda.nombre

    @hybrid_property
    def condicion_propietario_unidad_descripcion(self):
        return self.condicion_propietario_unidad.descripcion

    @hybrid_property
    def destino_nombre(self):
        return self.destino.nombre

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.gestor_carga.nombre

    @hybrid_property
    def merma_gestor_cuenta_moneda_nombre(self):
        return self.merma_gestor_cuenta_moneda.nombre

    @hybrid_property
    def merma_gestor_cuenta_tolerancia_kg(self):
        return (
            self.merma_gestor_cuenta_tolerancia
            if self.merma_gestor_cuenta_es_porcentual
            else self.merma_gestor_cuenta_tolerancia
            * self.merma_gestor_cuenta_unidad.conversion_kg
        )

    @hybrid_property
    def merma_gestor_cuenta_unidad_descripcion(self):
        return self.merma_gestor_cuenta_unidad.descripcion

    @hybrid_property
    def merma_propietario_moneda_nombre(self):
        return self.merma_propietario_moneda.nombre

    @hybrid_property
    def merma_propietario_tolerancia_kg(self):
        return (
            self.merma_propietario_tolerancia
            if self.merma_propietario_es_porcentual
            else self.merma_propietario_tolerancia
            * self.merma_propietario_unidad.conversion_kg
        )

    @hybrid_property
    def merma_propietario_unidad_descripcion(self):
        return self.merma_propietario_unidad.descripcion

    @hybrid_property
    def porcentaje_efectivo(self):
        anticipo_efectivo = get_flete_anticipo_efectivo(self.anticipos)
        return (
            anticipo_efectivo.porcentaje
            if (anticipo_efectivo and anticipo_efectivo.porcentaje)
            else 0
        )

    @hybrid_property
    def origen_nombre(self):
        return self.origen.nombre

    @hybrid_property
    def producto_descripcion(self):
        return self.producto.descripcion

    @hybrid_property
    def publicado_descripcion(self):
        return "Si" if self.publicado else "No"

    @hybrid_property
    def remitente_nombre(self):
        return self.remitente.nombre

    @hybrid_property
    def tipo_carga_descripcion(self):
        return self.tipo_carga.descripcion

    @hybrid_property
    def tipo_flete(self) -> TipoFleteEnum:
        if self.origen.pais_id == self.destino.pais_id:
            return TipoFleteEnum.DOMESTICO
        elif self.gestor_carga.pais_id == self.origen.pais_id:
            return TipoFleteEnum.EXPORTACION
        elif self.gestor_carga.pais_id == self.destino.pais_id:
            return TipoFleteEnum.IMPORTACION
        else:
            return TipoFleteEnum.DESCONOCIDO
