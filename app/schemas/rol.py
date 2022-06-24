from typing import List, Optional

from pydantic import BaseModel

from app.enums.estado import EstadoEnum

from .date_model import Date
from .gestor_carga import GestorCarga
from .permiso import PermisoChecked


# Shared properties
class RolBase(BaseModel):
    descripcion: str
    gestor_carga_id: Optional[int] = None
    permisos: List[PermisoChecked] = []


# Properties to receive via API on creation
class RolCreate(RolBase):
    pass


# Properties to receive via API on update
class RolUpdate(RolBase):
    pass


class RolInDBBase(RolBase):
    id: int
    codigo: Optional[str] = None
    gestor_carga: Optional[GestorCarga] = None
    estado: EstadoEnum
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True


# Additional properties to return via API
class Rol(RolInDBBase):
    pass
