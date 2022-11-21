from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base
from app.enums import TipoDocumentoRelacionadoEnum

from .seleccionable_mixin import SeleccionableMixin
from .tipo_documento_relacionado import TipoDocumentoRelacionado


class TipoCuenta(SeleccionableMixin, Base):
    """
    Defines the tipo cuenta model
    """

    codigo: str = Column(String(3), unique=True)
    tipo_documento_relacionado_id: int = Column(
        Integer, ForeignKey("tipo_documento_relacionado.id")
    )
    tipo_documento_relacionado: TipoDocumentoRelacionado = relationship(
        TipoDocumentoRelacionado, uselist=False
    )

    @hybrid_property
    def codigo_descripcion(self):
        if (
            self.tipo_documento_relacionado.descripcion
            == TipoDocumentoRelacionadoEnum.OTRO.value
        ):
            return f"{self.codigo}: {self.descripcion}"
        return self.descripcion
