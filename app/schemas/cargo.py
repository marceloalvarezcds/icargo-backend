from .estado_base_model import EstadoBaseModel


class Cargo(EstadoBaseModel):
    id: int
    descripcion: str

    class Config:
        orm_mode = True
