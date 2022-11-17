from sqlalchemy import Column, ForeignKey, Integer, Numeric, String  # type: ignore
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql.schema import UniqueConstraint  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database.base import Base
from app.enums.estado import EstadoEnum

from .camion import Camion
from .gestor_carga import GestorCarga
from .producto import Producto
from .semi import Semi


class CamionSemiNeto(AuditMixin, Base):
    """
    Defines the camion - semi - producto model
    """

    __table_args__ = (
        UniqueConstraint(
            "camion_id", "semi_id", "producto_id", "gestor_carga_id", "neto"
        ),
    )
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("producto.id"))
    producto = relationship(Producto, uselist=False)
    camion_id = Column(Integer, ForeignKey("camion.id"))
    camion = relationship(Camion, uselist=False, back_populates="combinaciones")
    semi_id = Column(Integer, ForeignKey("semi.id"))
    semi = relationship(Semi, uselist=False, back_populates="combinaciones")
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    neto = Column(Numeric(38, 10))
    estado = Column(String(15), server_default=EstadoEnum.ACTIVO.value)

    @hybrid_property
    def camion_info(self):
        return self.camion.info

    @hybrid_property
    def camion_placa(self):
        return self.camion.placa

    @hybrid_property
    def gestor_carga_nombre(self):
        return self.gestor_carga.nombre

    @hybrid_property
    def producto_descripcion(self):
        return self.producto.descripcion if self.producto else None

    @hybrid_property
    def producto_info(self):
        return (
            f"Nº {self.producto.id}: ({self.producto.descripcion})"
            if self.producto
            else None
        )

    @hybrid_property
    def semi_info(self):
        return self.semi.info

    @hybrid_property
    def semi_placa(self):
        return self.semi.placa
