from sqlalchemy import (  # type: ignore
    Column,
    ForeignKey,
    Integer,
    String,
    text,
)
from .propietario import Propietario
from .chofer import Chofer
from .camion import Camion
from .semi import Semi
from sqlalchemy.orm import relationship  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

class Combinacion(AuditMixin, Base):

    __tablename__= "combinacion"
    id = Column(Integer, primary_key=True)

    chofer_id = Column(Integer, ForeignKey('chofer.id'))
    chofer: Chofer = relationship(Chofer, uselist=False)

    propietario_id = Column(Integer, ForeignKey('propietario.id'))
    propietario: Propietario = relationship(Propietario, uselist=False)

    camion_id = Column(Integer, ForeignKey('camion.id'))
    camion: Camion = relationship(Camion, uselist=False)

    semi_id = Column(Integer, ForeignKey('semi.id'))
    semi: Semi = relationship(Semi, uselist=False)
    estado = Column(String(255), server_default=EstadoEnum.ACTIVO.value)
    comentario = Column(String(255))
    capacidad_total_combinacion = Column(Integer, server_default=text("0"))

    
   





