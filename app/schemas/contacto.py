from pydantic import BaseModel, EmailStr


class Contacto(BaseModel):
    id: int
    nombre: str
    apellido: str
    telefono: str
    email: EmailStr

    class Config:
        orm_mode = True
