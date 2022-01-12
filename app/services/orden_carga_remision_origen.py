from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaRemisionOrigen
from app.services.pictshare import upload_and_get_image_url


async def create_orden_carga_remision_origen(
    db: Session,
    data: schemas.OrdenCargaRemisionOrigenForm,
    foto_documento_file: UploadFile,
    modified_by: str,
) -> schemas.OrdenCargaRemisionOrigen:
    if repositories.get_orden_carga_remision_origen_by(db, data.numero_documento):
        raise HTTPException(status_code=409, detail="El Remisión de origen ya existe")
    foto_documento_url = await upload_and_get_image_url(foto_documento_file)
    return repositories.create_orden_carga_remision_origen(
        db,
        data,
        foto_documento_url,
        modified_by,
    )


def get_orden_carga_remision_origen_by_id(
    db: Session, id: int
) -> OrdenCargaRemisionOrigen:
    obj = repositories.get_orden_carga_remision_origen_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Remisión de origen no encontrado")
    return obj


async def edit_orden_carga_remision_origen(
    id: int,
    db: Session,
    data: schemas.OrdenCargaRemisionOrigenForm,
    foto_documento_file: Optional[UploadFile],
    modified_by: str,
) -> schemas.OrdenCargaRemisionOrigen:
    exists = repositories.get_orden_carga_remision_origen_by(db, data.numero_documento)
    if exists and exists.id != id:
        raise HTTPException(status_code=409, detail="La Remisión de origen ya existe")
    foto_documento_url = (
        await upload_and_get_image_url(foto_documento_file)
        if foto_documento_file
        else None
    )
    to_edit_obj = get_orden_carga_remision_origen_by_id(db, id)
    return repositories.edit_orden_carga_remision_origen(
        to_edit_obj,
        db,
        data,
        foto_documento_url,
        modified_by,
    )


def delete_orden_carga_remision_origen(
    db: Session, id: int, modified_by: str
) -> schemas.OrdenCargaRemisionOrigen:
    return repositories.delete_orden_carga_remision_origen(db, id, modified_by)
