from typing import Optional

from .estado_base_model import EstadoBaseModel


class GestorCargaPuntoVenta(EstadoBaseModel):
    id: int
    punto_venta_id: int
    gestor_carga_id: int
    alias: Optional[str] = None

    class Config:
        orm_mode = True
