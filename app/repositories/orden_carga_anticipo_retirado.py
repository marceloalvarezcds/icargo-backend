from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaAnticipoRetirado
from app.schemas import OrdenCargaAnticipoRetiradoForm


def get_orden_carga_anticipo_retirado_by(
    db: Session,
    flete_anticipo_id: int,
    orden_carga_id: int,
    punto_venta_id: int,
    tipo_comprobante_id: Optional[int] = None,
    numero_comprobante: Optional[str] = None,
) -> Optional[OrdenCargaAnticipoRetirado]:
    return (
        db.query(OrdenCargaAnticipoRetirado)
        .filter(
            OrdenCargaAnticipoRetirado.flete_anticipo_id == flete_anticipo_id,
            OrdenCargaAnticipoRetirado.orden_carga_id == orden_carga_id,
            OrdenCargaAnticipoRetirado.punto_venta_id == punto_venta_id,
            OrdenCargaAnticipoRetirado.tipo_comprobante_id == tipo_comprobante_id,
            OrdenCargaAnticipoRetirado.numero_comprobante == numero_comprobante,
        )
        .first()
    )


def get_orden_carga_anticipo_retirado_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaAnticipoRetirado]:
    return (
        db.query(OrdenCargaAnticipoRetirado)
        .filter(OrdenCargaAnticipoRetirado.id == id)
        .first()
    )


def create_orden_carga_anticipo_retirado(
    db: Session,
    data: OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> OrdenCargaAnticipoRetirado:
    obj = OrdenCargaAnticipoRetirado(
        flete_anticipo_id=data.flete_anticipo_id,
        orden_carga_id=data.orden_carga_id,
        punto_venta_id=data.punto_venta_id,
        tipo_comprobante_id=data.tipo_comprobante_id,
        numero_comprobante=data.numero_comprobante,
        moneda_id=data.moneda_id,
        monto_retirado=data.monto_retirado,
        observacion=data.observacion,
        insumo_punto_venta_precio_id=data.insumo_punto_venta_precio_id,
        unidad_id=data.unidad_id,
        cantidad_retirada=data.cantidad_retirada,
        precio_unitario=data.precio_unitario,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_anticipo_retirado(
    obj: OrdenCargaAnticipoRetirado,
    db: Session,
    data: OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> OrdenCargaAnticipoRetirado:
    obj.flete_anticipo_id = data.flete_anticipo_id
    obj.orden_carga_id = data.orden_carga_id
    obj.punto_venta_id = data.punto_venta_id
    obj.tipo_comprobante_id = data.tipo_comprobante_id
    obj.numero_comprobante = data.numero_comprobante
    obj.moneda_id = data.moneda_id
    obj.monto_retirado = data.monto_retirado
    obj.observacion = data.observacion
    obj.insumo_punto_venta_precio_id = data.insumo_punto_venta_precio_id
    obj.unidad_id = data.unidad_id
    obj.cantidad_retirada = data.cantidad_retirada
    obj.precio_unitario = data.precio_unitario
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga_anticipo_retirado(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaAnticipoRetirado).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
