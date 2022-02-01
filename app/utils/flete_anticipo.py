from decimal import Decimal
from typing import List, Optional

from app.enums.tipo_anticipo import TipoAnticipoEnum
from app.enums.tipo_insumo import TipoInsumoEnum
from app.schemas.flete_anticipo import FleteAnticipo


def get_flete_anticipo_efectivo(
    flete_anticipo_list: List[FleteAnticipo],
) -> Optional[FleteAnticipo]:
    for item in flete_anticipo_list:
        if item.tipo_descripcion == TipoAnticipoEnum.EFECTIVO.value:
            return item
    return None


def get_flete_anticipo_by_tipo_insumo_descripcion(
    flete_anticipo_list: List[FleteAnticipo],
    tipo_insumo_descripcion: TipoInsumoEnum,
) -> Optional[FleteAnticipo]:
    for item in flete_anticipo_list:
        if item.tipo_insumo_descripcion == tipo_insumo_descripcion.value:
            return item
    return None


def get_porcentaje_maximo_by_flete_anticipo_list(
    flete_anticipo_list: List[FleteAnticipo],
) -> Decimal:
    max = Decimal(0)
    for item in flete_anticipo_list:
        max += item.porcentaje if item.porcentaje else Decimal(0)
    return max
