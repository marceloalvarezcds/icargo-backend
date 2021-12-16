from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .moneda import Moneda
from .proveedor import Proveedor
from .tipo_concepto_descuento import TipoConceptoDescuento


class FleteDescuentoForm(BaseModel):
    id: Optional[int] = None
    concepto_id: int
    detalle: Optional[str]
    habilitar_pago_proveedor: bool
    anticipado: bool
    # INICIO Monto a cobrar al Propietario
    propietario_monto: Optional[Decimal] = None
    propietario_moneda_id: Optional[int] = None
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_monto: Optional[Decimal] = None
    proveedor_moneda_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    # FIN Monto a pagar al Proveedor


class FleteDescuento(FleteDescuentoForm):
    id: int
    concepto: TipoConceptoDescuento
    # INICIO Monto a cobrar al Propietario
    propietario_moneda: Moneda
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_moneda: Optional[Moneda]
    proveedor: Optional[Proveedor] = None
    # FIN Monto a pagar al Proveedor
    flete_id: int
