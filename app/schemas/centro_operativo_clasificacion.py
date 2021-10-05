from pydantic import BaseModel


class CentroOperativoClasificacion(BaseModel):
    id: int
    nombre: str
    es_moderado: bool

    class Config:
        orm_mode = True
