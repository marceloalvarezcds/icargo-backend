from pydantic import BaseModel

from app.enums import FleteDestinatarioEnum


class FleteDestinatario(BaseModel):
    id: int
    tipo_destinatario: FleteDestinatarioEnum
    email: str
    nombre: str

    class Config:
        use_enum_values = True
