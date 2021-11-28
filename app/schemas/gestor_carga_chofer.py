from .estado_base_model import EstadoBaseModel


class GestorCargaChofer(EstadoBaseModel):
    id: int
    chofer_id: int
    gestor_carga_id: int
    alias: str

    class Config:
        orm_mode = True
