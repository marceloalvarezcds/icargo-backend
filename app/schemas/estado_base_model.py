from pydantic import BaseModel

from app.enums.estado import EstadoEnum


class EstadoBaseModel(BaseModel):
    estado: EstadoEnum

    class Config:
        use_enum_values = True
