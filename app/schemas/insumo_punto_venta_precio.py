from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.enums.estado import EstadoEnum

from .date_model import Date


class InsumoPuntoVentaPrecioForm(BaseModel):
    id: Optional[int] = None
    tipo_id: int
    insumo_id: int
    proveedor_id: int
    punto_venta_id: int
    moneda_id: int
    precio: Decimal
    fecha_inicio: Date


class InsumoPuntoVentaPrecio(BaseModel):
    id: int
    precio: Decimal
    fecha_fin: Optional[Date] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class InsumoPuntoVentaPrecioList(InsumoPuntoVentaPrecio):
    insumo_punto_venta_id: int
    estado: EstadoEnum
    gestor_carga_id: int
    gestor_carga_nombre: str
    insumo_descripcion: str
    insumo_moneda_nombre: str
    insumo_tipo_descripcion: str
    insumo_unidad_abreviatura: Optional[str] = None
    insumo_unidad_descripcion: Optional[str] = None
    punto_venta_nombre: str
