from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaAnticipoRetirado


def create_orden_carga_anticipo_retirado(
    db: Session,
    data: schemas.OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> schemas.OrdenCargaAnticipoRetirado:
    if repositories.get_orden_carga_anticipo_retirado_by(
        db, data.flete_anticipo_id, data.orden_carga_id, data.punto_venta_id
    ):
        raise HTTPException(status_code=409, detail="El Anticipo ya existe")
    return repositories.create_orden_carga_anticipo_retirado(
        db,
        data,
        modified_by,
    )


def get_orden_carga_anticipo_retirado_by_id(
    db: Session, id: int
) -> OrdenCargaAnticipoRetirado:
    obj = repositories.get_orden_carga_anticipo_retirado_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Anticipo no encontrado")
    return obj


def edit_orden_carga_anticipo_retirado(
    id: int,
    db: Session,
    data: schemas.OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> schemas.OrdenCargaAnticipoRetirado:
    exists = repositories.get_orden_carga_anticipo_retirado_by(
        db, data.flete_anticipo_id, data.orden_carga_id, data.punto_venta_id
    )
    if exists and exists.id != id:
        raise HTTPException(status_code=409, detail="El Anticipo ya existe")
    to_edit_obj = get_orden_carga_anticipo_retirado_by_id(db, id)
    return repositories.edit_orden_carga_anticipo_retirado(
        to_edit_obj,
        db,
        data,
        modified_by,
    )


def delete_orden_carga_anticipo_retirado(
    db: Session, id: int, modified_by: str
) -> schemas.OrdenCargaAnticipoRetirado:
    return repositories.delete_orden_carga_anticipo_retirado(db, id, modified_by)
