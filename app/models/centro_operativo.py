from sqlalchemy import (  # type: ignore
    DECIMAL,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .centro_operativo_clasificacion import CentroOperativoClasificacion
from .ciudad import Ciudad
from .contacto import Contacto


class CentroOperativo(AuditMixin, Base):
    """
    Defines the centro operativo model
    """

    __table_args__ = (
        UniqueConstraint(
            "nombre",
            "clasificacion_id",
            "ciudad_id",
        ),
    )
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    nombre_corto = Column(String(255))
    logo = Column(String(255))
    es_moderado = Column(Boolean(), server_default=text("false"))
    direccion = Column(String(255))
    latitud = Column(DECIMAL)
    longitud = Column(DECIMAL)
    clasificacion_id = Column(Integer, ForeignKey("centro_operativo_clasificacion.id"))
    clasificacion = relationship(CentroOperativoClasificacion, uselist=False)
    ciudad_id = Column(Integer, ForeignKey("ciudad.id"))
    ciudad = relationship(Ciudad, uselist=False)
    contacto_id = Column(Integer, ForeignKey("contacto.id"))
    contacto = relationship(Contacto, uselist=False)
