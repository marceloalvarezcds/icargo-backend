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

class OrdenCargaEvaluacionesHistorial(OrdenCargaEvaluacionesHistorialForm):
    id: int
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date
    

    class Config:
        orm_mode = True
        use_enum_values = True