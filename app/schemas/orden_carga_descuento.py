from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .moneda import Moneda
from .proveedor import Proveedor
from .tipo_concepto_descuento import TipoConceptoDescuento


class OrdenCargaDescuentoForm(BaseModel):
    id: Optional[int] = None
    concepto: TipoConceptoDescuento
    detalle: Optional[str]
    habilitar_pago_proveedor: Optional[bool] = False
    anticipado: Optional[bool] = False
    # INICIO Monto a cobrar al Propietario
    propietario_monto: Optional[Decimal] = None
    propietario_moneda: Moneda
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_monto: Optional[Decimal] = None
    proveedor_moneda: Optional[Moneda]
    proveedor: Optional[Proveedor] = None
    # FIN Monto a pagar al Proveedor
    orden_carga_id: int
    flete_id: Optional[int] = None


class OrdenCargaDescuento(OrdenCargaDescuentoForm):
    id: int
    concepto_id: int
    concepto_descripcion: str
    anticipado_descripcion: str
    # INICIO Monto a cobrar al Propietario
    propietario_moneda_id: int
    propietario_moneda_nombre: str
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    proveedor_moneda_id: Optional[int] = None
    proveedor_moneda_nombre: Optional[str] = None
    proveedor_id: Optional[int] = None
    proveedor_nombre: Optional[str] = None
    # FIN Monto a pagar al Proveedor

    class Config:
        orm_mode = True
        use_enum_values = True
