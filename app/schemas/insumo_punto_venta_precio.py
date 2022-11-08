from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.enums.estado import EstadoEnum

from .date_model import Date
from .rounded_decimal_model import RoundedDecimal


class InsumoPuntoVentaPrecioForm(BaseModel):
    tipo_id: Optional[int] = None
    insumo_id: int
    proveedor_id: Optional[int] = None
    punto_venta_id: int
    moneda_id: int
    precio: RoundedDecimal
    fecha_inicio: Date
    fecha_fin: Optional[Date] = None


class InsumoPuntoVentaPrecio(BaseModel):
    id: int
    precio: RoundedDecimal
    fecha_inicio: Date
    fecha_fin: Optional[Date] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class InsumoPuntoVentaPrecioList(InsumoPuntoVentaPrecio):
    insumo_punto_venta_id: int
    estado: EstadoEnum
    ciudad_nombre: Optional[str] = None
    gestor_carga_id: int
    gestor_carga_nombre: str
    insumo_id: int
    insumo_descripcion: str
    insumo_moneda_id: int
    insumo_moneda_nombre: str
    insumo_moneda_simbolo: str
    insumo_tipo_id: int
    insumo_tipo_descripcion: str
    insumo_unidad_abreviatura: Optional[str] = None
    insumo_unidad_descripcion: Optional[str] = None
    localidad_nombre: Optional[str] = None
    pais_nombre: Optional[str] = None
    pais_nombre_corto: Optional[str] = None
    proveedor_id: int
    proveedor_nombre: str
    punto_venta_id: int
    punto_venta_nombre: str
    punto_venta_direccion: Optional[str] = None
    punto_venta_logo: Optional[str] = None
    punto_venta_latitud: Optional[Decimal] = None
    punto_venta_longitud: Optional[Decimal] = None
