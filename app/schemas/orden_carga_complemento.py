from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .moneda import Moneda
from .tipo_concepto_complemento import TipoConceptoComplemento


class OrdenCargaComplementoForm(BaseModel):
    id: Optional[int] = None
    concepto_id: int
    detalle: Optional[str]
    habilitar_cobro_remitente: Optional[bool] = False
    anticipado: Optional[bool] = False
    # INICIO Monto a pagar al Propietario
    propietario_monto: Optional[Decimal] = None
    propietario_moneda_id: Optional[int] = None
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_monto: Optional[Decimal] = None
    remitente_moneda_id: Optional[int] = None
    # FIN Monto a cobrar al Remitente
    orden_carga_id: int
    flete_id: Optional[int] = None


class OrdenCargaComplemento(OrdenCargaComplementoForm):
    id: int
    concepto: TipoConceptoComplemento
    concepto_descripcion: str
    anticipado_descripcion: str
    # INICIO Monto a pagar al Propietario
    propietario_moneda: Moneda
    propietario_moneda_nombre: str
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    remitente_moneda: Optional[Moneda] = None
    remitente_moneda_nombre: Optional[str] = None
    # FIN Monto a cobrar al Remitente

    class Config:
        orm_mode = True
        use_enum_values = True
