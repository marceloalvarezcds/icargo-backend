from typing import Optional

from pydantic import BaseModel

from .date_model import Date
from .rounded_decimal_model import RoundedDecimal


class OrdenCargaEvaluacionesHistorialForm(BaseModel):
    orden_carga_id: Optional[int] = None
    comentario: Optional[str] = None
    tipo_incidente_id: Optional[int] = None
    gestor_carga_id: Optional[int] = None
    camion_id: Optional[int] = None
    semi_id: Optional[int] = None
    propietario_id: Optional[int] = None
    chofer_id: Optional[int] = None
    nota: Optional[str] = None
    concepto: Optional[str] = None
    origen_id: Optional[int] = None
    destino_id: Optional[int] = None
    producto_id: Optional[int] = None
    comentarios: Optional[str] = None
    tracto_rating: Optional[int] = None
    semi_rating: Optional[int] = None
    chofer_rating: Optional[int] = None
    propietario_rating: Optional[int] = None
    carga_rating: Optional[int] = None
    descarga_rating: Optional[int] = None

class OrdenCargaEvaluacionesHistorial(OrdenCargaEvaluacionesHistorialForm):
    id: int
    oc_camion_placa: Optional[str] = None
    oc_semi_placa: Optional[str] = None
    oc_chofer_nombre: Optional[str] = None
    oc_beneficiario_nombre: Optional[str] = None
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date
    

    class Config:
        orm_mode = True
        use_enum_values = True