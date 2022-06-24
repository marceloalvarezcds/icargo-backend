from typing import Optional

from pydantic import BaseModel, validator

from app.enums import PermisoAccionEnum, PermisoModeloEnum, PermisoModuloEnum


class Permiso(BaseModel):
    id: int
    modelo: PermisoModeloEnum
    accion: PermisoAccionEnum
    modulo: PermisoModuloEnum
    modelo_titulo: str
    descripcion: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class PermisoChecked(Permiso):
    checked: Optional[bool] = True

    @validator("checked")
    def set_checked(cls, _):
        return True
