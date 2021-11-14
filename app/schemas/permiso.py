from typing import Optional

from pydantic import BaseModel

from app.enums import PermisoAccionEnum, PermisoModeloEnum


class Permiso(BaseModel):
    id: int
    modelo: PermisoModeloEnum
    accion: PermisoAccionEnum
    autorizado: bool
    descripcion: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True
