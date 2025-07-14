from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaRemisionDestino
from app.services.pictshare import upload_and_get_image_url
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

async def create_orden_carga_remision_destino(
    db: Session,
    data: schemas.OrdenCargaRemisionDestinoForm,
    foto_documento_file: Optional[UploadFile],
    modified_by: str,
):
    existe = repositories.get_orden_carga_remision_destino_by(db, data.numero_documento)
    foto_documento_url = await upload_and_get_image_url(foto_documento_file)
    nueva = repositories.create_orden_carga_remision_destino(
        db,
        data,
        foto_documento_url,
        modified_by,
    )
    pydantic_nueva = schemas.OrdenCargaRemisionDestino.from_orm(nueva)

    if existe:
        content = {
            "warning": "⚠️ Ya existe remisión con ese número, pero se guardó.",
            "data": pydantic_nueva.dict()
        }
        return JSONResponse(status_code=200, content=jsonable_encoder(content))

    return pydantic_nueva


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
):
    exists = repositories.get_orden_carga_remision_destino_by(db, data.numero_documento)
    foto_documento_url = (
        await upload_and_get_image_url(foto_documento_file) if foto_documento_file else None
    )
    to_edit_obj = get_orden_carga_remision_destino_by_id(db, id)
    edited = repositories.edit_orden_carga_remision_destino(
        to_edit_obj,
        db,
        data,
        foto_documento_url,
        modified_by,
    )

    pydantic_edited = schemas.OrdenCargaRemisionDestino.from_orm(edited)

    if exists and exists.id != id:
        content = {
            "warning": "⚠️ Ya existe remisión con ese número, pero se guardó.",
            "data": pydantic_edited.dict()
        }
        return JSONResponse(status_code=200, content=jsonable_encoder(content))

    return pydantic_edited


def delete_orden_carga_remision_destino(db: Session, id: int, modified_by: str) -> schemas.OrdenCargaRemisionDestino:
    obj = db.query(OrdenCargaRemisionDestino).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="OrdenCargaRemisionDestino not found")
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    result = schemas.OrdenCargaRemisionDestino.from_orm(obj)
    db.delete(obj)
    db.commit()

    return result

