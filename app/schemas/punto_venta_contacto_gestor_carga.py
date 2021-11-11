from typing import Optional

from .cargo import Cargo
from .contacto import Contacto
from .estado_base_model import EstadoBaseModel


class PuntoVentaContactoGestorCarga(EstadoBaseModel):
    id: int
    cargo_id: int
    cargo: Cargo
    punto_venta_id: int
    contacto_id: int
    contacto: Contacto
    gestor_carga_id: int
    alias: Optional[str] = None

    class Config:
        orm_mode = True


class PuntoVentaContactoGestorCargaList(PuntoVentaContactoGestorCarga):
    cargo_descripcion: str
    contacto_nombre: str
    contacto_apellido: str
    contacto_telefono: str
    contacto_email: str
