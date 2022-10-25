from decimal import Decimal

from sqlalchemy import (  # type: ignore
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    text,
)
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum
from app.utils import number_format

from .chofer import Chofer
from .ciudad import Ciudad
from .color import Color
from .ente_emisor_automotor import EnteEmisorAutomotor
from .ente_emisor_transporte import EnteEmisorTransporte
from .marca_camion import MarcaCamion
from .propietario import Propietario
from .tipo_camion import TipoCamion


class Camion(AuditMixin, Base):
    """
    Defines the camion model
    """

    id = Column(Integer, primary_key=True)
    placa = Column(String(255), unique=True)
    propietario_id = Column(Integer, ForeignKey("propietario.id"))
    propietario = relationship(Propietario, uselist=False)
    chofer_id = Column(Integer, ForeignKey("chofer.id"))
    chofer = relationship(Chofer, uselist=False)
    numero_chasis = Column(String(255))
    foto = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.PENDIENTE.value)
    # INICIO Limitaciones del Camión
    limite_cantidad_oc_activas = Column(Integer, server_default=text("1"))
    # SE USA LA MONEDA DEL GESTOR, por el momento
    limite_monto_anticipos = Column(Numeric(38, 10))
    total_anticipos_retirados_en_estado_pendiente_o_en_proceso = Column(Numeric(38, 10))
    # FIN Limitaciones del Camión
    # INICIO Habilitaciones del Camión
    # inicio - municipal
    ciudad_habilitacion_municipal_id = Column(Integer, ForeignKey("ciudad.id"))
    ciudad_habilitacion_municipal = relationship(Ciudad, uselist=False)
    numero_habilitacion_municipal = Column(String(255))
    vencimiento_habilitacion_municipal = Column(DateTime)
    foto_habilitacion_municipal_frente = Column(String(255))
    foto_habilitacion_municipal_reverso = Column(String(255))
    # fin - municipal
    # inicio - transporte
    ente_emisor_transporte_id = Column(Integer, ForeignKey("ente_emisor_transporte.id"))
    ente_emisor_transporte = relationship(EnteEmisorTransporte, uselist=False)
    numero_habilitacion_transporte = Column(String(255))
    vencimiento_habilitacion_transporte = Column(DateTime)
    foto_habilitacion_transporte_frente = Column(String(255))
    foto_habilitacion_transporte_reverso = Column(String(255))
    # fin - transporte
    # inicio - automotor
    ente_emisor_automotor_id = Column(Integer, ForeignKey("ente_emisor_automotor.id"))
    ente_emisor_automotor = relationship(EnteEmisorAutomotor, uselist=False)
    titular_habilitacion_automotor = Column(String(255))
    foto_habilitacion_automotor_frente = Column(String(255))
    foto_habilitacion_automotor_reverso = Column(String(255))
    # fin - automotor
    # FIN Habilitaciones del Camión
    # INICIO Detalles del Camión
    marca_id = Column(Integer, ForeignKey("marca_camion.id"))
    marca = relationship(MarcaCamion, uselist=False)
    tipo_id = Column(Integer, ForeignKey("tipo_camion.id"))
    tipo = relationship(TipoCamion, uselist=False)
    color_id = Column(Integer, ForeignKey("color.id"))
    color = relationship(Color, uselist=False)
    anho = Column(Integer)
    # FIN Detalles del Camión
    # INICIO Capacidad del Camión
    bruto = Column(Numeric(38, 10))
    tara = Column(Numeric(38, 10))
    # FIN Capacidad del Camión
    combinaciones = relationship("CamionSemiNeto", back_populates="camion")

    @hybrid_property
    def chofer_estado(self):
        return self.chofer.estado if self.chofer else None

    @hybrid_property
    def chofer_nombre(self):
        return self.chofer.nombre if self.chofer else None

    @hybrid_property
    def chofer_numero_documento(self):
        return self.chofer.numero_documento if self.chofer else None

    @hybrid_property
    def chofer_puede_recibir_anticipos(self):
        return self.chofer.puede_recibir_anticipos if self.chofer else False

    @hybrid_property
    def ciudad_habilitacion_municipal_nombre(self):
        return (
            self.ciudad_habilitacion_municipal.nombre
            if self.ciudad_habilitacion_municipal
            else None
        )

    @hybrid_property
    def color_descripcion(self):
        return self.color.descripcion if self.color else ""

    @hybrid_property
    def gestor_cuenta_id(self):
        return self.propietario.gestor_cuenta.id

    @hybrid_property
    def gestor_cuenta_nombre(self):
        return self.propietario.gestor_cuenta.nombre

    @hybrid_property
    def limites(self):
        anticipos = (
            f" || Anticipos: {number_format(self.limite_monto_anticipos)}"
            if self.limite_monto_anticipos
            else ""
        )
        return f"OC: {self.limite_cantidad_oc_activas if self.limite_cantidad_oc_activas else ''} {anticipos}"  # noqa: B950

    @hybrid_property
    def localidad_habilitacion_municipal_id(self):
        return (
            self.ciudad_habilitacion_municipal.localidad_id
            if self.ciudad_habilitacion_municipal
            else None
        )

    @hybrid_property
    def localidad_habilitacion_municipal_nombre(self):
        return (
            self.ciudad_habilitacion_municipal.localidad.nombre
            if self.ciudad_habilitacion_municipal
            else None
        )

    @hybrid_property
    def monto_anticipo_disponible(self) -> Decimal:
        return (self.limite_monto_anticipos if self.limite_monto_anticipos else 0) - (
            self.total_anticipos_retirados_en_estado_pendiente_o_en_proceso
            if self.total_anticipos_retirados_en_estado_pendiente_o_en_proceso
            else 0
        )

    @hybrid_property
    def info(self):
        return f"{self.placa} - {self.propietario_nombre}"

    @hybrid_property
    def marca_descripcion(self):
        return self.marca.descripcion if self.marca else None

    @hybrid_property
    def neto(self):
        return (self.bruto if self.bruto else 0) - (self.tara if self.tara else 0)

    @hybrid_property
    def oficial_cuenta_nombre(self):
        return self.propietario.oficial_cuenta_nombre

    @hybrid_property
    def pais_habilitacion_municipal_id(self):
        return (
            self.ciudad_habilitacion_municipal.localidad.pais_id
            if self.ciudad_habilitacion_municipal
            else None
        )

    @hybrid_property
    def pais_habilitacion_municipal_nombre(self):
        return (
            self.ciudad_habilitacion_municipal.localidad.pais.nombre
            if self.ciudad_habilitacion_municipal
            else None
        )

    @hybrid_property
    def pais_habilitacion_municipal_nombre_corto(self):
        return (
            self.ciudad_habilitacion_municipal.localidad.pais.nombre_corto
            if self.ciudad_habilitacion_municipal
            else None
        )

    @hybrid_property
    def pais_emisor_placa_nombre(self):
        return (
            self.ente_emisor_automotor.pais.nombre
            if self.ente_emisor_automotor
            else None
        )

    @hybrid_property
    def pais_emisor_placa_nombre_corto(self):
        return (
            self.ente_emisor_automotor.pais.nombre_corto
            if self.ente_emisor_automotor
            else None
        )

    @hybrid_property
    def propietario_estado(self):
        return self.propietario.estado

    @hybrid_property
    def propietario_nombre(self):
        return self.propietario.nombre

    @hybrid_property
    def propietario_ruc(self):
        return self.propietario.ruc

    @hybrid_property
    def propietario_puede_recibir_anticipos(self):
        return self.propietario.puede_recibir_anticipos

    @hybrid_property
    def propietario_telefono(self):
        return self.propietario.telefono

    @hybrid_property
    def tipo_descripcion(self):
        return self.tipo.descripcion if self.tipo else None
