from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base

from .centro_operativo_contacto_gestor_carga import CentroOperativoContactoGestorCarga
from .flete import Flete
from .remitente_contacto_gestor_carga import RemitenteContactoGestorCarga
from .user import User


class FleteCentroOperativoContacto(AuditMixin, Base):
    """
    Defines the flete_centro_operativo_contacto model
    """

    __table_args__ = (PrimaryKeyConstraint("flete_id", "centro_operativo_contacto_id"),)
    id = Column(Integer)
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False)
    centro_operativo_contacto_id = Column(
        Integer, ForeignKey("centro_operativo_contacto_gestor_carga.id")
    )
    centro_operativo_contacto = relationship(
        CentroOperativoContactoGestorCarga, uselist=False
    )


class FleteRemitenteContacto(AuditMixin, Base):
    """
    Defines the flete_remitente_contacto model
    """

    __table_args__ = (PrimaryKeyConstraint("flete_id", "remitente_contacto_id"),)
    id = Column(Integer)
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False)
    remitente_contacto_id = Column(
        Integer, ForeignKey("remitente_contacto_gestor_carga.id")
    )
    remitente_contacto = relationship(RemitenteContactoGestorCarga, uselist=False)


class FleteUserContacto(AuditMixin, Base):
    """
    Defines the flete_user_contacto model
    """

    __table_args__ = (PrimaryKeyConstraint("flete_id", "user_contacto_id"),)
    id = Column(Integer)
    flete_id = Column(Integer, ForeignKey("flete.id"))
    flete = relationship(Flete, uselist=False)
    user_contacto_id = Column(Integer, ForeignKey("user.id"))
    user_contacto = relationship(User, uselist=False)
