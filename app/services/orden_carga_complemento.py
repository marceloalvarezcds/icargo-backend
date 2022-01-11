from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaComplemento


def create_orden_carga_complemento(
    db: Session,
    data: schemas.OrdenCargaComplementoForm,
    modified_by: str,
) -> schemas.OrdenCargaComplemento:
    if repositories.get_orden_carga_complemento_by(
        db,
        data.concepto_id,
        data.propietario_moneda_id,
        data.propietario_monto,
        data.remitente_moneda_id,
        data.remitente_monto,
        data.orden_carga_id,
    ):
        raise HTTPException(status_code=409, detail="El Complemento ya existe")
    return repositories.create_orden_carga_complemento(
        db,
        data,
        modified_by,
    )


def get_orden_carga_complemento_by_id(db: Session, id: int) -> OrdenCargaComplemento:
    obj = repositories.get_orden_carga_complemento_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Complemento no encontrado")
    return obj


def edit_orden_carga_complemento(
    id: int,
    db: Session,
    data: schemas.OrdenCargaComplementoForm,
    modified_by: str,
) -> schemas.OrdenCargaComplemento:
    exists = repositories.get_orden_carga_complemento_by(
        db,
        data.concepto_id,
        data.propietario_moneda_id,
        data.propietario_monto,
        data.remitente_moneda_id,
        data.remitente_monto,
        data.orden_carga_id,
    )
    if exists and exists.id != id:
        raise HTTPException(status_code=409, detail="El Complemento ya existe")
    to_edit_obj = get_orden_carga_complemento_by_id(db, id)
    return repositories.edit_orden_carga_complemento(
        to_edit_obj,
        db,
        data,
        modified_by,
    )


def delete_orden_carga_complemento(
    db: Session, id: int, modified_by: str
) -> schemas.OrdenCargaComplemento:
    return repositories.delete_orden_carga_complemento(db, id, modified_by)
