from .estado_base_model import EstadoBaseModel


class GestorCargaPropietario(EstadoBaseModel):
    id: int
    propietario_id: int
    gestor_carga_id: int
    alias: str

    class Config:
        orm_mode = True
