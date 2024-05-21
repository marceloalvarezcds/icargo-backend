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

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .ciudad import Ciudad
from .color import Color
from .ente_emisor_automotor import EnteEmisorAutomotor
from .ente_emisor_transporte import EnteEmisorTransporte
from .marca_semi import MarcaSemi
from .propietario import Propietario
from .semi_clasificacion import SemiClasificacion
from .tipo_carga import TipoCarga
from .tipo_semi import TipoSemi


class Semi(AuditMixin, Base):
    """
    Defines the semi model
    """

    id = Column(Integer, primary_key=True)
    placa = Column(String(255), unique=True)
    propietario_id = Column(Integer, ForeignKey("propietario.id"))
    propietario = relationship(Propietario, uselist=False)
    numero_chasis = Column(String(255))
    foto = Column(String(255))
    estado = Column(String(255), server_default=EstadoEnum.PENDIENTE.value)
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
    marca_id = Column(Integer, ForeignKey("marca_semi.id"))
    marca = relationship(MarcaSemi, uselist=False)
    clasificacion_id = Column(Integer, ForeignKey("semi_clasificacion.id"))
    clasificacion = relationship(SemiClasificacion, uselist=False)
    tipo_id = Column(Integer, ForeignKey("tipo_semi.id"))
    tipo = relationship(TipoSemi, uselist=False)
    tipo_carga_id = Column(Integer, ForeignKey("tipo_carga.id"))
    tipo_carga = relationship(TipoCarga, uselist=False)
    color_id = Column(Integer, ForeignKey("color.id"))
    color = relationship(Color, uselist=False)
    anho = Column(Integer)
    # FIN Detalles del Camión
    # INICIO Capacidad del Camión
    bruto = Column(Numeric(38, 10))
    tara = Column(Numeric(38, 10))
    largo = Column(Numeric(38, 10))
    alto = Column(Numeric(38, 10))
    ancho = Column(Numeric(38, 10))
    volumen = Column(Numeric(38, 10))
    # FIN Capacidad del Camión
    combinaciones = relationship("CamionSemiNeto", back_populates="semi")

    @hybrid_property
    def ciudad_habilitacion_municipal_nombre(self):
        return (
            self.ciudad_habilitacion_municipal.nombre
            if self.ciudad_habilitacion_municipal
            else None
        )

    @hybrid_property
    def clasificacion_descripcion(self):
        return self.clasificacion.descripcion if self.clasificacion else None

    @hybrid_property
    def color_descripcion(self):
        return self.color.descripcion if self.color else ""
    
    @hybrid_property
    def foto_semi(self):
        return self.semi.foto if self.semi else None
    
    @hybrid_property
    def gestor_cuenta_id(self):
        return self.propietario.gestor_cuenta.id

    @hybrid_property
    def gestor_cuenta_nombre(self):
        return self.propietario.gestor_cuenta.nombre

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
    def propietario_nombre(self):
        return self.propietario.nombre

    @hybrid_property
    def propietario_ruc(self):
        return self.propietario.ruc

    @hybrid_property
    def tipo_descripcion(self):
        return self.tipo.descripcion if self.tipo else None

    @hybrid_property
    def tipo_carga_descripcion(self):
        return self.tipo_carga.descripcion if self.tipo_carga else None
