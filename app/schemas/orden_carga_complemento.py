from typing import Optional

from pydantic import BaseModel

from .moneda import Moneda
from .rounded_decimal_model import RoundedDecimal
from .tipo_concepto_complemento import TipoConceptoComplemento


class OrdenCargaComplementoForm(BaseModel):
    id: Optional[int] = None
    concepto: TipoConceptoComplemento
    detalle: Optional[str] = None
    habilitar_cobro_remitente: Optional[bool] = False
    anticipado: Optional[bool] = False
    # INICIO Monto a pagar al Propietario
    propietario_monto: RoundedDecimal
    propietario_moneda: Moneda
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_monto: Optional[RoundedDecimal] = None
    remitente_moneda: Optional[Moneda] = None
    # FIN Monto a cobrar al Remitente
    orden_carga_id: int
    flete_id: Optional[int] = None


class OrdenCargaComplemento(OrdenCargaComplementoForm):
    id: int
    concepto_id: int
    concepto_descripcion: str
    anticipado_descripcion: str
    # INICIO Monto a pagar al Propietario
    propietario_moneda_id: int
    propietario_moneda_nombre: str
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_moneda_id: Optional[int] = None
    remitente_moneda_nombre: Optional[str] = None
    # FIN Monto a cobrar al Remitente

    class Config:
        orm_mode = True
        use_enum_values = True
