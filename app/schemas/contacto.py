from typing import Optional

from pydantic import BaseModel, EmailStr

from .cargo import Cargo


class ContactoBaseModel(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    email: EmailStr


class ContactoForm(ContactoBaseModel):
    id: Optional[int] = None
    cargo: Cargo


class Contacto(ContactoBaseModel):
    id: int

    class Config:
        orm_mode = True
