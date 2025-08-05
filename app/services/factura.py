from typing import Optional

from fastapi import HTTPException, UploadFile  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, logger
from app.models import Factura, TipoIva
from app.schemas import FacturaForm
from . import movimiento as service
from app.services import generic_service as generic_service
from .pictshare import upload_and_get_image_url
from app.config import LOGO_IMAGE_URL, REPORTS_FOLDER, templateEnv, STATICS_FOLDER, dir_path
import os
from jinja2 import Template
from pdfkit import from_string  # type: ignore
from app.utils import number_format

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

    tipoIva = generic_service.get_by_id(TipoIva, db, data.iva_id)

    if tipoIva.iva > 0:
        if data.iva<=0:
            raise HTTPException(
            status_code=409, detail=f"Para el de tipo de IVA {tipoIva.descripcion} debe cargar un valor IVA"
        )

    foto_url = 'foto' # await upload_and_get_image_url(foto_file) if foto_file else None
    #foto_url = await upload_and_get_image_url(foto_file) if foto_file else None
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


def get_factura_pdf_by_id(db: Session, id: int) -> str:
    logger.info('Inicio del proceso de generación de PDF de factura')

    factura = repositories.get_factura_by_id(db, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    data = {
        "numero_factura": factura.numero_factura or "",
        "fecha_factura": factura.fecha_factura.strftime("%Y-%m-%d") if factura.fecha_factura else "",
        "fecha_vencimiento": factura.fecha_vencimiento.strftime("%Y-%m-%d") if factura.fecha_vencimiento else "",
        "monto": number_format(factura.monto),
        "iva": number_format(factura.iva),
        "iva_id": factura.iva_id,
        "iva_incluido": factura.iva_incluido,
        "retencion": number_format(factura.retencion),
        "porcentaje_retencion": f"{factura.tipo_retencion}%" if factura.tipo_retencion and factura.tipo_retencion not in ["NO", "NO APLICA"] else "No aplica",
        "timbrado": factura.timbrado or "",
        "ruc": factura.ruc,
        "contribuyente": factura.contribuyente,
        "sentido_mov_iva": factura.sentido_mov_iva,
        "sentido_mov_retencion": factura.sentido_mov_retencion,
        "moneda": factura.moneda_nombre,
        "moneda_simbolo": factura.moneda_simbolo,
        "iva_descripcion": factura.iva_descripcion,
        "contraparte": factura.contraparte,
        "contraparte_numero_documento": factura.contraparte_numero_documento,
        "tipo_contraparte": factura.tipo_contraparte_descripcion,
        "tipo_operacion": factura.tipo_operacion_descripcion,
    }

    OUTPUT_FILENAME = f"factura_{id}.pdf"

    template: Template = templateEnv.get_template("factura.html")
    STATICS_FOLDER_LOGO = os.path.join(dir_path, "statics/logo-icargo.png")
    source_html = template.render(logo=STATICS_FOLDER_LOGO, **data)

    logger.info('Template HTML generado correctamente')

    pdf_filename = os.path.join(REPORTS_FOLDER, OUTPUT_FILENAME)
    from_string(source_html, pdf_filename, {"enable-local-file-access": "", "page-size": "Legal"})

    logger.info(f'PDF generado correctamente en: {pdf_filename}')
    return OUTPUT_FILENAME
