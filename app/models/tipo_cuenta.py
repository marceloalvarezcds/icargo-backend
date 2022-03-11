from sqlalchemy import Column, ForeignKey, Integer  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.database.base import Base

from .seleccionable_mixin import SeleccionableMixin
from .tipo_documento_relacionado import TipoDocumentoRelacionado


class TipoCuenta(SeleccionableMixin, Base):
    """
    Defines the tipo cuenta model
    """

    tipo_documento_relacionado_id = Column(
        Integer, ForeignKey("tipo_documento_relacionado.id")
    )
    tipo_documento_relacionado = relationship(TipoDocumentoRelacionado, uselist=False)
