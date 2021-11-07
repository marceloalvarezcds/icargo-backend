from .cargo import Cargo
from .contacto import Contacto
from .estado_base_model import EstadoBaseModel


class ProveedorContactoGestorCarga(EstadoBaseModel):
    id: int
    cargo_id: int
    cargo: Cargo
    proveedor_id: int
    contacto_id: int
    contacto: Contacto
    gestor_carga_id: int

    class Config:
        orm_mode = True


class ProveedorContactoGestorCargaList(ProveedorContactoGestorCarga):
    cargo_descripcion: str
    contacto_nombre: str
    contacto_apellido: str
    contacto_telefono: str
    contacto_email: str
