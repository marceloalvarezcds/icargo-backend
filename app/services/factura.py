from typing import Optional

from fastapi import HTTPException, UploadFile  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Factura
from app.schemas import FacturaForm
from . import movimiento as service
from . import liquidacion as liquidacionService
from .pictshare import upload_and_get_image_url


async def create_factura(
    db: Session,
    data: FacturaForm,
    foto_file: Optional[UploadFile],
    modified_by: str,
    gestor_carga_id: Optional[int] = None
) -> Factura:

    if repositories.get_factura_by(
        db, data.liquidacion_id, data.numero_factura, data.moneda_id, data.iva_id
    ):
        raise HTTPException(
            status_code=409, detail=f"La Factura Nº {data.numero_factura} ya existe"
        )

    #foto_url = 'foto' # await upload_and_get_image_url(foto_file) if foto_file else None
    foto_url = await upload_and_get_image_url(foto_file) if foto_file else None
    factura = repositories.create_factura(db, data, foto_url, modified_by)

    if data.sentido_mov_iva or data.sentido_mov_retencion:
        service.create_movimiento_by_factura(db, data, gestor_carga_id, modified_by, factura)
        #liquidacionService.refresh_pago_cobro(db, data.liquidacion_id, modified_by)

    return factura


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
    #foto_url = 'foto url' 

    if to_edit_obj.iva_movimiento_id or to_edit_obj.retencion_movimiento_id:
        service.edit_movimiento_by_factura(db, to_edit_obj, data, modified_by)
        #liquidacionService.refresh_pago_cobro(db, data.liquidacion_id, modified_by)

    return repositories.edit_factura(to_edit_obj, db, data, foto_url, modified_by)


def delete_factura(db: Session, id: int, modified_by: str) -> Factura:
    co = get_factura_by_id(db, id)

    if co.iva_movimiento_id or co.retencion_movimiento_id:
        service.delete_movimiento_by_factura(db, co, modified_by)
        #liquidacionService.refresh_pago_cobro(db, co.liquidacion_id, modified_by)

    factura = repositories.delete_factura(co, db, modified_by)

    return factura
