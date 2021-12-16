from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .moneda import Moneda
from .tipo_concepto_complemento import TipoConceptoComplemento


class FleteComplementoForm(BaseModel):
    id: Optional[int] = None
    concepto_id: int
    detalle: Optional[str]
    habilitar_cobro_remitente: bool
    anticipado: bool
    # INICIO Monto a pagar al Propietario
    propietario_monto: Optional[Decimal] = None
    propietario_moneda_id: Optional[int] = None
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_monto: Optional[Decimal] = None
    remitente_moneda_id: Optional[int] = None
    # FIN Monto a cobrar al Remitente


class FleteComplemento(FleteComplementoForm):
    id: int
    concepto: TipoConceptoComplemento
    # INICIO Monto a pagar al Propietario
    propietario_moneda: Moneda
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_moneda: Optional[Moneda] = None
    # FIN Monto a cobrar al Remitente
    flete_id: int
