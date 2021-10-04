from pydantic import BaseModel


class Pais(BaseModel):
    id: int
    nombre: str
    nombre_corto: str

    class Config:
        orm_mode = True
