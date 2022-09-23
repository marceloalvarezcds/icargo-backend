from typing import Optional

from pydantic import BaseModel


class Auth(BaseModel):
    username: str
    password: str


class AuthBaseModel(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    is_admin: bool
    gestor_carga_id: Optional[int] = None

    class Config:
        orm_mode = True


class AuthUser(AuthBaseModel):
    chofer_id: Optional[int] = None
    propietario_id: Optional[int] = None
    punto_venta_id: Optional[int] = None


class AuthPuntoVentaUser(AuthBaseModel):
    punto_venta_id: int
