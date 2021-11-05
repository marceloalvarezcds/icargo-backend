from .estado_base_model import EstadoBaseModel


class Moneda(EstadoBaseModel):
    id: int
    nombre: str
    simbolo: str

    class Config:
        orm_mode = True
