from .estado_base_model import EstadoBaseModel


class SeleccionableBaseModel(EstadoBaseModel):
    id: int
    descripcion: str

    class Config:
        orm_mode = True
