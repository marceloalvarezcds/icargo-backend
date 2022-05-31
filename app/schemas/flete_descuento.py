from typing import Optional

from pydantic import BaseModel

from .moneda import Moneda
from .proveedor import Proveedor
from .rounded_decimal_model import RoundedDecimal
from .tipo_concepto_descuento import TipoConceptoDescuento


class FleteDescuentoForm(BaseModel):
    id: Optional[int] = None
    concepto_id: int
    detalle: Optional[str]
    habilitar_pago_proveedor: Optional[bool] = False
    # INICIO Monto a cobrar al Propietario
    propietario_monto: Optional[RoundedDecimal] = None
    propietario_moneda_id: Optional[int] = None
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_monto: Optional[RoundedDecimal] = None
    proveedor_moneda_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    # FIN Monto a pagar al Proveedor


class FleteDescuento(FleteDescuentoForm):
    id: int
    concepto: TipoConceptoDescuento
    concepto_descripcion: str
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
    flete_id: int

    class Config:
        orm_mode = True
