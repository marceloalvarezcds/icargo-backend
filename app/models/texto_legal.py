from sqlalchemy import Column, Integer, String, ForeignKey  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base
from app.enums.estado import EstadoEnum
from .seleccionable_mixin import SeleccionableMixin
from .gestor_carga import GestorCarga


class TextoLegal(SeleccionableMixin, Base):

    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    titulo = Column(String(45), unique=True)
