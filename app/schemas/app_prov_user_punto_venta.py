from typing import Any, Optional

from pydantic import BaseModel, EmailStr

from .ciudad import Ciudad
from .token import Token


class Proveedor(BaseModel):
    id: int
    nombre: str
    nombre_corto: Optional[str] = None
    numero_documento: str


class PuntoVenta(BaseModel):
    id: int
    nombre: str
    nombre_corto: Optional[str] = None
    numero_documento: str
    ciudad: Optional[Ciudad] = None

    class Config:
        orm_mode = True


class UserPuntoVentaInfo(BaseModel):
    id: int
    username: str
    is_admin: bool
    is_admin_descripcion: str

    class Config:
        orm_mode = True


class UserPuntoVenta(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    authentication_token: str
    punto_venta: PuntoVenta

    class Config:
        orm_mode = True

    @classmethod
    def from_orm_with_token(cls, obj: Any, token: Token) -> "UserPuntoVenta":
        obj.authentication_token = f"{token.token_type} {token.access_token}"
        return super().from_orm(obj)


class UserPuntoVentaCreateForm(BaseModel):
    username: str
    password: str
    confirm_password: str
