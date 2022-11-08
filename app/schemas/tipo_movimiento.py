from .seleccionable_base_model import SeleccionableBaseModel, SeleccionableFormBaseModel


class TipoMovimiento(SeleccionableBaseModel):
    cuenta_id: int
    cuenta_descripcion: str
    info: str


class TipoMovimientoForm(SeleccionableFormBaseModel):
    cuenta_id: int
