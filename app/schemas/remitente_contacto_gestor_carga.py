from .cargo import Cargo
from .contacto import Contacto
from .estado_base_model import EstadoBaseModel


class RemitenteContactoGestorCarga(EstadoBaseModel):
    id: int
    cargo_id: int
    cargo: Cargo
    remitente_id: int
    contacto_id: int
    contacto: Contacto
    gestor_carga_id: int

    class Config:
        orm_mode = True


class RemitenteContactoGestorCargaList(RemitenteContactoGestorCarga):
    cargo_descripcion: str
    contacto_nombre: str
    contacto_apellido: str
    contacto_telefono: str
    contacto_email: str
