from typing import List, Optional

from app.enums.estado import EstadoEnum
from pydantic import BaseModel

from .date_model import Date
from .rounded_decimal_model import RoundedDecimal


class OrdenCargaAnticipoRetiradoBaseModel(BaseModel):
    flete_anticipo_id: int
    orden_carga_id: int
    punto_venta_id: int
    orden_carga_anticipo_porcentaje_id: Optional[int] = None
    tipo_comprobante_id: Optional[int] = None
    numero_comprobante: Optional[str] = None
    moneda_id: int
    monto_retirado: RoundedDecimal
    observacion: Optional[str] = None
    insumo_punto_venta_precio_id: Optional[int] = None
    unidad_id: Optional[int] = None
    cantidad_retirada: Optional[RoundedDecimal] = None
    precio_unitario: Optional[RoundedDecimal] = None
    # campos auxiliares
    tipo_anticipo_id: int
    tipo_insumo_id: Optional[int] = None
    insumo_id: Optional[int] = None
    proveedor_id: int


class OrdenCargaAnticipoRetiradoForm(OrdenCargaAnticipoRetiradoBaseModel):
    es_con_litro: bool = False


class OrdenCargaAnticipoRetirado(OrdenCargaAnticipoRetiradoBaseModel):
    id: int
    concepto: str
    gestor_carga_id: int
    gestor_carga_nombre: str
    gestor_carga_moneda_nombre: str
    insumo_descripcion: Optional[str] = None
    insumo_fecha_precio: Optional[Date] = None
    insumo_moneda_nombre: Optional[str] = None
    insumo_precio: Optional[RoundedDecimal] = None
    insumo_tipo_descripcion: Optional[str] = None
    insumo_unidad_abreviatura: Optional[str] = None
    insumo_unidad_descripcion: Optional[str] = None
    moneda_nombre: str
    proveedor_nombre: str
    punto_venta_nombre: str
    punto_venta_pais_nombre: Optional[str] = None
    tipo_anticipo_descripcion: str
    tipo_comprobante_descripcion: Optional[str] = None
    tipo_insumo_descripcion: Optional[str] = None
    unidad_abreviatura: Optional[str] = None
    unidad_descripcion: Optional[str] = None
    estados_movimientos: Optional[str] = None
    
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True


class OrdenCargaAnticipoRetiradoAnulado(BaseModel):
    id: int
    estado: EstadoEnum
    insumo_descripcion: Optional[str] = None
    insumo_fecha_precio: Optional[Date] = None
    insumo_moneda_nombre: Optional[str] = None
    insumo_precio: Optional[RoundedDecimal] = None
    insumo_tipo_descripcion: Optional[str] = None
    insumo_unidad_abreviatura: Optional[str] = None
    insumo_unidad_descripcion: Optional[str] = None
    punto_venta_pais_nombre: Optional[str] = None
    tipo_anticipo_descripcion: str
    tipo_comprobante_descripcion: Optional[str] = None
    tipo_insumo_descripcion: Optional[str] = None
    unidad_abreviatura: Optional[str] = None
    unidad_descripcion: Optional[str] = None
    # Auditoría
    created_by: str
    created_at: Date
    modified_by: str
    modified_at: Date

    class Config:
        orm_mode = True
        use_enum_values = True
