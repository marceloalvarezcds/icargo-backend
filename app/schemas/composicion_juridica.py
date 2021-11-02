from .estado_base_model import EstadoBaseModel


class ComposicionJuridica(EstadoBaseModel):
    id: int
    nombre: str
    nombre_corto: str

    class Config:
        orm_mode = True
