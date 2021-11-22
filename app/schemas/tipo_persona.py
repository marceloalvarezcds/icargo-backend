from .estado_base_model import EstadoBaseModel


class TipoPersona(EstadoBaseModel):
    id: int
    descripcion: str

    class Config:
        orm_mode = True
