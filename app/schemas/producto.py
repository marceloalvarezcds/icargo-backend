from .date_model import Date
from .seleccionable_base_model import SeleccionableBaseModel
from .tipo_carga import TipoCarga


class Producto(SeleccionableBaseModel):
    tipo_carga_id: int
    tipo_carga: TipoCarga
    tipo_carga_descripcion: str
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date
