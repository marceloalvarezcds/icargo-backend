from app.models.gestor_carga import GestorCarga
from app.models.producto import Producto
from sqlalchemy.ext.hybrid import hybrid_property  # type: ignore
from sqlalchemy import (  # type: ignore
    Column,
    ForeignKey,
    Integer,
    String,
    text,
    Numeric,
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
    gestor_carga_id = Column(Integer, ForeignKey("gestor_carga.id"))
    gestor_carga = relationship(GestorCarga, uselist=False)
    neto = Column(Numeric(38, 10))

    
    @hybrid_property
    def camion_placa(self):
        return self.camion.placa 
    
    @hybrid_property
    def camion_oc_activa(self):
        return self.camion.limite_cantidad_oc_activas if self.camion else None
    
    @hybrid_property
    def limite_anticipos(self):
        return self.camion.limite_monto_anticipos if self.camion.limite_monto_anticipos else 0
    
    @hybrid_property
    def marca_descripcion(self):
        return self.camion.marca_descripcion if self.camion else None
    
    @hybrid_property
    def foto_camion(self):
        return self.camion.foto if self.camion else None
    
    @hybrid_property
    def camion_propietario_nombre(self):
        return self.camion.propietario.nombre
    
    @hybrid_property
    def camion_propietario_documento(self):
        return self.camion.propietario.ruc
    
    @hybrid_property
    def marca_descripcion_semi(self):
        return self.semi.marca.descripcion if self.semi else None    
    
    @hybrid_property
    def chofer_estado(self):
        return self.chofer.estado 

    @hybrid_property
    def chofer_nombre(self):
        return self.chofer.nombre if self.chofer else None

    @hybrid_property
    def chofer_numero_documento(self):
        return self.chofer.numero_documento 
    
    @hybrid_property
    def puede_recibir_anticipos(self):
        return self.chofer.puede_recibir_anticipos 
    
    @hybrid_property
    def propietario_nombre(self):
        return self.propietario.nombre
    
    @hybrid_property
    def color_camion(self):
        return self.camion.color.descripcion

    @hybrid_property
    def propietario_ruc(self):
        return self.propietario.ruc

    @hybrid_property
    def anticipo_propietario(self):
        return self.propietario.puede_recibir_anticipos 

    @hybrid_property
    def propietario_telefono(self):
        return self.propietario.telefono
    
    # @hybrid_property
    # def tipo_persona_id(self):
    #     return self.propietario.tipo_persona_id 

    @hybrid_property
    def tipo_descripcion(self):
        return self.tipo.descripcion 
    
    @hybrid_property
    def producto_descripcion(self):
        return self.producto.descripcion 
    
    @hybrid_property
    def semi_placa(self):
        return self.semi.placa 
    


    
   