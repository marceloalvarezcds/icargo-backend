from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaRemisionDestino
from app.services.pictshare import upload_and_get_image_url
from datetime import datetime

async def create_orden_carga_remision_destino(
    db: Session,
    data: schemas.OrdenCargaRemisionDestinoForm,
    foto_documento_file: Optional[UploadFile],
    modified_by: str,
) -> schemas.OrdenCargaRemisionDestino:
    if repositories.get_orden_carga_remision_destino_by(db, data.numero_documento):
        raise HTTPException(status_code=409, detail="El Remisión de destino ya existe")
    foto_documento_url = await upload_and_get_image_url(foto_documento_file)
    return repositories.create_orden_carga_remision_destino(
        db,
        data,
        foto_documento_url,
        modified_by,
    )


def get_orden_carga_remision_destino_by_id(
    db: Session, id: int
) -> OrdenCargaRemisionDestino:
    obj = repositories.get_orden_carga_remision_destino_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Remisión de destino no encontrado")
    return obj


async def edit_orden_carga_remision_destino(
    id: int,
    db: Session,
    data: schemas.OrdenCargaRemisionDestinoForm,
    foto_documento_file: Optional[UploadFile],
    modified_by: str,
) -> schemas.OrdenCargaRemisionDestino:
    exists = repositories.get_orden_carga_remision_destino_by(db, data.numero_documento)
    if exists and exists.id != id:
        raise HTTPException(status_code=409, detail="La Remisión de destino ya existe")
    foto_documento_url = (
        await upload_and_get_image_url(foto_documento_file)
        if foto_documento_file
        else None
    )
    to_edit_obj = get_orden_carga_remision_destino_by_id(db, id)
    return repositories.edit_orden_carga_remision_destino(
        to_edit_obj,
        db,
        data,
        foto_documento_url,
        modified_by,
    )


def delete_orden_carga_remision_destino(db: Session, id: int, modified_by: str) -> schemas.OrdenCargaRemisionDestino:
    obj = db.query(OrdenCargaRemisionDestino).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="OrdenCargaRemisionDestino not found")
    
    # Actualizar los campos de auditoría
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    
    # Serializar los datos antes de eliminar
    result = schemas.OrdenCargaRemisionDestino.from_orm(obj)
    
    # Eliminar el objeto
    db.delete(obj)
    db.commit()
    
    return result

