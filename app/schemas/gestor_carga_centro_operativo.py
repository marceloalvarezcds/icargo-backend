from typing import Optional

from .estado_base_model import EstadoBaseModel


class GestorCargaCentroOperativo(EstadoBaseModel):
    id: int
    centro_operativo_id: int
    gestor_carga_id: int
    alias: Optional[str] = None

    class Config:
        orm_mode = True
