from pydantic import BaseModel

from app.enums import EstadoEnum


class CentroOperativoClasificacion(BaseModel):
    id: int
    nombre: str
    estado: EstadoEnum

    class Config:
        orm_mode = True
        use_enum_values = True
