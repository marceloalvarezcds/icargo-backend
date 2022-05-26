from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.enums import EstadoEnum

from .rounded_decimal_model import RoundedDecimal


class CamionSemiNetoForm(BaseModel):
    camion_id: int
    semi_id: int
    producto_id: Optional[int] = None
    neto: RoundedDecimal


class CamionSemiNeto(CamionSemiNetoForm):
    id: int
    camion_info: str
    camion_placa: str
    semi_info: str
    semi_placa: str
    producto_descripcion: Optional[str] = None
    gestor_carga_id: int
    gestor_carga_nombre: str
    estado: EstadoEnum
    # Auditoría
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True
