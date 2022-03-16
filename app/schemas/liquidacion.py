from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.enums.estado import EstadoEnum

from .date_model import Date
from .moneda import Moneda
from .movimiento import MovimientoForm
from .tipo_contraparte import TipoContraparte


class LiquidacionForm(BaseModel):
    tipo_contraparte_id: int
    contraparte: str
    contraparte_numero_documento: str
    moneda_id: int
    # IDs para referencia a las tablas de las contraparte
    chofer_id: Optional[int]
    gestor_carga_id: Optional[int]
    propietario_id: Optional[int]
    proveedor_id: Optional[int]
    remitente_id: Optional[int]
    # Lista
    movimientos: List[MovimientoForm]


class Liquidacion(LiquidacionForm):
    tipo_contraparte: TipoContraparte
    fecha_pago_cobro: Date
    estado: EstadoEnum
    moneda: Moneda
    # movimientos: List[Movimiento]
    # instrumentos: List[Instrumento]
    es_cobro: bool
    instrumentos_saldo: Decimal
    moneda_nombre: str
    moneda_simbolo: str
    movimientos_saldo: Decimal
    tipo_contraparte_descripcion: str
    tipo_operacion_descripcion: str
    url: str
