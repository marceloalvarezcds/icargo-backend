from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, root_validator

from app.enums.estado import EstadoEnum

from .date_model import Date
from .permiso import Permiso
from .rol import RolChecked


class AuthUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    gestor_carga_id: Optional[int] = None

    class Config:
        orm_mode = True


# Shared properties
class UserBase(BaseModel):
    token: Optional[str] = None
    email: Optional[EmailStr] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_superuser: Optional[bool] = False
    gestor_carga_id: Optional[int] = None
    last_ip_address: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    roles: List[RolChecked] = []

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password and password != confirm_password:
            raise ValueError("Las contraseñas no coinciden")
        return values


# Properties to receive via API on creation
class UserCreate(UserUpdate):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    created_ip_address: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    reset_password_code: Optional[str] = None
    activation_code: Optional[str] = None
    persist_code: Optional[str] = None
    created_ip_address: Optional[str] = None
    estado: EstadoEnum
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    roles: List[RolChecked] = []

    @classmethod
    def from_orm(cls, obj: Any) -> "User":
        obj.roles = []
        return super().from_orm(obj)


class UserAccount(UserInDBBase):
    permisos: List[Permiso] = []
    is_admin_icargo: bool

    @classmethod
    def from_orm(cls, obj: Any) -> "UserAccount":
        obj.permisos = []
        obj.is_admin_icargo = False
        return super().from_orm(obj)


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
