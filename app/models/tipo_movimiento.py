from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.database.base import Base
from app.enums import TipoDocumentoRelacionadoEnum

from .seleccionable_mixin import SeleccionableMixin
from .tipo_cuenta import TipoCuenta


class TipoMovimiento(SeleccionableMixin, Base):
    """
    Defines the tipo movimiento model
    """

    __table_args__ = (UniqueConstraint("cuenta_id", "codigo"),)
    codigo: str = Column(String(2))
    cuenta_id: int = Column(Integer, ForeignKey("tipo_cuenta.id"))
    cuenta: TipoCuenta = relationship(TipoCuenta, uselist=False)

    @hybrid_property
    def codigo_descripcion(self):
        if (
            self.cuenta.tipo_documento_relacionado.descripcion
            == TipoDocumentoRelacionadoEnum.OTRO.value
        ):
            return f"{self.codigo}: {self.descripcion}"
        return self.descripcion

    @hybrid_property
    def cuenta_codigo_descripcion(self):
        return self.cuenta.codigo_descripcion

    @hybrid_property
    def info(self):
        return f"{self.cuenta_codigo_descripcion} - {self.codigo_descripcion}"
