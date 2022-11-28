from typing import Optional

from .estado_base_model import EstadoBaseModel


class GestorCargaProveedor(EstadoBaseModel):
    id: int
    proveedor_id: int
    gestor_carga_id: int
    alias: Optional[str] = None

    class Config:
        orm_mode = True
