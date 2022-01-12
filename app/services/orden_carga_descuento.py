from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaDescuento


def create_orden_carga_descuento(
    db: Session,
    data: schemas.OrdenCargaDescuentoForm,
    modified_by: str,
) -> schemas.OrdenCargaDescuento:
    if repositories.get_orden_carga_descuento_by(
        db,
        data.concepto_id,
        data.propietario_moneda_id,
        data.propietario_monto,
        data.proveedor_moneda_id,
        data.proveedor_monto,
        data.orden_carga_id,
    ):
        raise HTTPException(status_code=409, detail="El Descuento ya existe")
    return repositories.create_orden_carga_descuento(
        db,
        data,
        modified_by,
    )


def get_orden_carga_descuento_by_id(db: Session, id: int) -> OrdenCargaDescuento:
    obj = repositories.get_orden_carga_descuento_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    return obj


def edit_orden_carga_descuento(
    id: int,
    db: Session,
    data: schemas.OrdenCargaDescuentoForm,
    modified_by: str,
) -> schemas.OrdenCargaDescuento:
    exists = repositories.get_orden_carga_descuento_by(
        db,
        data.concepto_id,
        data.propietario_moneda_id,
        data.propietario_monto,
        data.proveedor_moneda_id,
        data.proveedor_monto,
        data.orden_carga_id,
    )
    if exists and exists.id != id:
        raise HTTPException(status_code=409, detail="El Descuento ya existe")
    to_edit_obj = get_orden_carga_descuento_by_id(db, id)
    return repositories.edit_orden_carga_descuento(
        to_edit_obj,
        db,
        data,
        modified_by,
    )


def delete_orden_carga_descuento(
    db: Session, id: int, modified_by: str
) -> schemas.OrdenCargaDescuento:
    return repositories.delete_orden_carga_descuento(db, id, modified_by)
