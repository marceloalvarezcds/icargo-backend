from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from .date_model import Date


class OrdenCargaAnticipoRetiradoForm(BaseModel):
    flete_anticipo_id: int
    orden_carga_id: int
    punto_venta_id: int
    tipo_comprobante_id: int
    numero_comprobante: str
    moneda_id: int
    monto_retirado: Decimal
    observacion: Optional[str] = None
    insumo_punto_venta_precio_id: Optional[int] = None
    unidad_id: Optional[int] = None
    cantidad_retirada: Optional[Decimal] = None
    precio_unitario: Optional[Decimal] = None


class OrdenCargaAnticipoRetirado(OrdenCargaAnticipoRetiradoForm):
    id: int
    gestor_carga_id: int
    gestor_carga_nombre: str
    gestor_carga_moneda_nombre: str
    insumo_descripcion: Optional[str] = None
    insumo_fecha_precio: Optional[Date] = None
    insumo_moneda_nombre: Optional[str] = None
    insumo_precio: Optional[Decimal] = None
    insumo_tipo_descripcion: Optional[str] = None
    insumo_unidad_abreviatura: Optional[str] = None
    insumo_unidad_descripcion: Optional[str] = None
    moneda_nombre: str
    proveedor_nombre: str
    punto_venta_nombre: str
    punto_venta_pais_nombre: str
    tipo_anticipo_descripcion: str
    tipo_comprobante_descripcion: str
    tipo_insumo_descripcion: str
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
