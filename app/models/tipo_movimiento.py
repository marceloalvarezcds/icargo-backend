from sqlalchemy import Column, ForeignKey, Integer  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin
from .tipo_cuenta import TipoCuenta


class TipoMovimiento(SeleccionableMixin, Base):
    """
    Defines the tipo movimiento model
    """

    cuenta_id = Column(Integer, ForeignKey("tipo_cuenta.id"))
    cuenta = relationship(TipoCuenta, uselist=False)

    @hybrid_property
    def cuenta_descripcion(self):
        return self.cuenta.descripcion

    @hybrid_property
    def info(self):
        return f"{self.cuenta_descripcion} - {self.descripcion}"
