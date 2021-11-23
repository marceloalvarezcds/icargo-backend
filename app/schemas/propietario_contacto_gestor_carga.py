from typing import Optional

from .cargo import Cargo
from .contacto import Contacto
from .estado_base_model import EstadoBaseModel


class PropietarioContactoGestorCarga(EstadoBaseModel):
    id: int
    cargo_id: int
    cargo: Cargo
    propietario_id: int
    contacto_id: int
    contacto: Contacto
    gestor_carga_id: int
    alias: Optional[str] = None

    class Config:
        orm_mode = True


class PropietarioContactoGestorCargaList(PropietarioContactoGestorCarga):
    cargo_descripcion: str
    contacto_nombre: str
    contacto_apellido: str
    contacto_telefono: str
    contacto_email: str
