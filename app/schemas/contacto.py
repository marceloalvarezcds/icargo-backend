from typing import Optional

from pydantic import BaseModel, EmailStr

from .cargo import Cargo


class ContactoBaseModel(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    email: Optional[str] = None 


class ContactoForm(ContactoBaseModel):
    id: Optional[int] = None
    cargo: Optional[Cargo] = None
    alias: Optional[str] = None


class Contacto(ContactoBaseModel):
    id: int

    class Config:
        orm_mode = True
