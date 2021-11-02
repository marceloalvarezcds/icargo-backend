from .estado_base_model import EstadoBaseModel


class GestorCargaRemitente(EstadoBaseModel):
    id: int
    remitente_id: int
    gestor_carga_id: int
    alias: str

    class Config:
        orm_mode = True
