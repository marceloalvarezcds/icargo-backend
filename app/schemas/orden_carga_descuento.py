from typing import Optional

from pydantic import BaseModel

from .date_model import Date
from .moneda import Moneda
from .proveedor import Proveedor
from .rounded_decimal_model import RoundedDecimal
from .tipo_concepto_descuento import TipoConceptoDescuento


class OrdenCargaDescuentoForm(BaseModel):
    id: Optional[int] = None
    concepto_id: int
    detalle: Optional[str]
    habilitar_pago_proveedor: Optional[bool] = False
    anticipado: Optional[bool] = False
    # INICIO Monto a cobrar al Propietario
    propietario_monto: Optional[RoundedDecimal] = None
    propietario_moneda_id: int
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_monto: Optional[RoundedDecimal] = None
    proveedor_moneda_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    # FIN Monto a pagar al Proveedor
    orden_carga_id: int
    flete_id: Optional[int] = None
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date


class OrdenCargaDescuento(OrdenCargaDescuentoForm):
    id: int
    concepto: TipoConceptoDescuento
    concepto_descripcion: str
    anticipado_descripcion: str
    # INICIO Monto a cobrar al Propietario
    propietario_moneda: Moneda
    propietario_moneda_nombre: str
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_moneda: Optional[Moneda]
    proveedor_moneda_nombre: Optional[str] = None
    proveedor: Optional[Proveedor] = None
    proveedor_nombre: Optional[str] = None
    # FIN Monto a pagar al Proveedor

    class Config:
        orm_mode = True
        use_enum_values = True
