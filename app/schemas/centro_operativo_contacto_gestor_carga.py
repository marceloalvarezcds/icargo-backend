from typing import Optional

from .cargo import Cargo
from .contacto import Contacto
from .estado_base_model import EstadoBaseModel


class CentroOperativoContactoGestorCarga(EstadoBaseModel):
    id: int
    cargo_id: int
    cargo: Cargo
    centro_operativo_id: int
    contacto_id: int
    contacto: Contacto
    gestor_carga_id: int
    alias: Optional[str] = None

    class Config:
        orm_mode = True


class CentroOperativoContactoGestorCargaList(CentroOperativoContactoGestorCarga):
    cargo_descripcion: str
    contacto_nombre: str
    contacto_apellido: str
    contacto_telefono: str
    contacto_email: str
