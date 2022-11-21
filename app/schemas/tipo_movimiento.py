from .seleccionable_base_model import SeleccionableBaseModel, SeleccionableFormBaseModel


class TipoMovimiento(SeleccionableBaseModel):
    cuenta_codigo_descripcion: str
    cuenta_id: int
    codigo: str
    codigo_descripcion: str
    info: str


class TipoMovimientoForm(SeleccionableFormBaseModel):
    cuenta_id: int
    codigo: str
