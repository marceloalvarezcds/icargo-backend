from typing import Optional

from pydantic import BaseModel

from app.enums import FleteDestinatarioCentroOperativoEnum, FleteDestinatarioEnum


class FleteDestinatario(BaseModel):
    id: int
    tipo_destinatario: FleteDestinatarioEnum
    tipo_centro_operativo: Optional[FleteDestinatarioCentroOperativoEnum] = None
    email: str
    nombre: str

    class Config:
        use_enum_values = True
