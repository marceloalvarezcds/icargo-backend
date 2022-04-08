from typing import Optional, cast

from fastapi import HTTPException, UploadFile  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Factura
from app.schemas import FacturaForm

from .pictshare import upload_and_get_image_url


async def create_factura(
    db: Session,
    data: FacturaForm,
    foto_file: UploadFile,
    modified_by: str,
) -> Factura:
    if repositories.get_factura_by(
        db, data.liquidacion_id, data.numero_factura, data.moneda_id, data.iva_id
    ):
        raise HTTPException(
            status_code=409, detail=f"La Factura Nº {data.numero_factura} ya existe"
        )
    foto_url = await upload_and_get_image_url(foto_file) if foto_file else None
    return repositories.create_factura(db, data, cast(str, foto_url), modified_by)


def get_factura_by_id(db: Session, id: int) -> Factura:
    obj = repositories.get_factura_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return obj


async def edit_factura(
    id: int,
    db: Session,
    data: FacturaForm,
    foto_file: Optional[UploadFile],
    modified_by: str,
) -> Factura:
    exists = repositories.get_factura_by(
        db, data.liquidacion_id, data.numero_factura, data.moneda_id, data.iva_id
    )
    if exists and exists.id != id:
        raise HTTPException(
            status_code=409, detail=f"La Factura Nº {data.numero_factura} ya existe"
        )
    to_edit_obj = get_factura_by_id(db, id)
    foto_url = await upload_and_get_image_url(foto_file) if foto_file else None
    return repositories.edit_factura(to_edit_obj, db, data, foto_url, modified_by)


def delete_factura(db: Session, id: int, modified_by: str) -> Factura:
    co = get_factura_by_id(db, id)
    return repositories.delete_factura(co, db, modified_by)
