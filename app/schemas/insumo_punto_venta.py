from typing import List, Optional

from app.schemas.rounded_decimal_model import RoundedDecimal
from pydantic import BaseModel

from app.enums.estado import EstadoEnum

from .insumo_punto_venta_precio import InsumoPuntoVentaPrecio


class InsumoPuntoVenta(BaseModel):
    id: int
    insumo_id: int
    punto_venta_id: int
    moneda_id: int
    estado: EstadoEnum
    gestor_carga_id: int
    gestor_carga_nombre: str
    insumo_descripcion: str
    insumo_tipo_descripcion: str
    insumo_unidad_abreviatura: Optional[str]
    insumo_unidad_descripcion: Optional[str]
    moneda_nombre: str
    punto_venta_nombre: str
    precios: List[InsumoPuntoVentaPrecio] = []
    precio: Optional[RoundedDecimal]
    class Config:
        orm_mode = True
        use_enum_values = True
