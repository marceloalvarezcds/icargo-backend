from typing import Optional

from pydantic import BaseModel

from .moneda import Moneda
from .rounded_decimal_model import RoundedDecimal
from .tipo_concepto_complemento import TipoConceptoComplemento


class FleteComplementoForm(BaseModel):
    id: Optional[int] = None
    concepto_id: int
    detalle: Optional[str]
    habilitar_cobro_remitente: Optional[bool] = False
    anticipado: Optional[bool] = False
    # INICIO Monto a pagar al Propietario
    propietario_monto: Optional[RoundedDecimal] = None
    propietario_monto_ml: Optional[RoundedDecimal] = None
    propietario_moneda_id: Optional[int] = None
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_monto: Optional[RoundedDecimal] = None
    remitente_monto_ml: Optional[RoundedDecimal] = None
    remitente_moneda_id: Optional[int] = None
    # FIN Monto a cobrar al Remitente


class FleteComplemento(FleteComplementoForm):
    id: int
    concepto: TipoConceptoComplemento
    concepto_descripcion: str
    # INICIO Monto a pagar al Propietario
    propietario_moneda: Moneda
    propietario_moneda_nombre: str
    propietario_moneda_simbolo: str
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_moneda: Optional[Moneda] = None
    remitente_moneda_nombre: Optional[str] = None
    remitente_moneda_simbolo: Optional[str] = None
    # FIN Monto a cobrar al Remitente
    flete_id: int
    gestor_carga_moneda_simbolo: str

    class Config:
        orm_mode = True
