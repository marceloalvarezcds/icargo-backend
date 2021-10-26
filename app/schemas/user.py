from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    token: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    is_activated: Optional[bool] = True
    is_guest: Optional[bool] = False
    is_superuser: Optional[bool] = False
    gestor_carga_id: Optional[int] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    reset_password_code: Optional[str] = None
    activation_code: Optional[str] = None
    persist_code: Optional[str] = None
    permissions: Optional[str] = None
    activated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    created_ip_address: Optional[str] = None
    last_ip_address: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
