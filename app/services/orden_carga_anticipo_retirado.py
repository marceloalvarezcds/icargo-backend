import os
from decimal import Decimal

from fastapi import HTTPException
from jinja2 import Template
from pdfkit import from_string  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.config import LOGO_IMAGE_URL, REPORTS_FOLDER, templateEnv
from app.models import OrdenCargaAnticipoRetirado

from .orden_carga_anticipo_saldo import update_orden_carga_anticipo_saldo_by_form


def create_orden_carga_anticipo_retirado(
    db: Session,
    data: schemas.OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> schemas.OrdenCargaAnticipoRetirado:
    if repositories.get_orden_carga_anticipo_retirado_by(
        db,
        data.flete_anticipo_id,
        data.orden_carga_id,
        data.punto_venta_id,
        data.tipo_comprobante_id,
        data.numero_comprobante,
    ):
        raise HTTPException(
            status_code=409,
            detail=f"El Anticipo con comporbante {data.numero_comprobante} ya existe",
        )
    update_orden_carga_anticipo_saldo_by_form(db, data, Decimal(0), modified_by)
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
        db,
        data.flete_anticipo_id,
        data.orden_carga_id,
        data.punto_venta_id,
        data.tipo_comprobante_id,
        data.numero_comprobante,
    )
    if exists and exists.id != id:
        raise HTTPException(
            status_code=409,
            detail=f"El Anticipo con comporbante {data.numero_comprobante} ya existe",
        )
    to_edit_obj = get_orden_carga_anticipo_retirado_by_id(db, id)
    update_orden_carga_anticipo_saldo_by_form(
        db, data, to_edit_obj.monto_retirado, modified_by
    )
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


def get_orden_carga_anticipo_retirado_pdf_by_id(db: Session, id: int) -> str:
    obj = repositories.get_orden_carga_anticipo_retirado_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Anticipo no encontrado")
    orden_carga = repositories.get_orden_carga_by_id(db, obj.orden_carga_id)
    if not orden_carga:
        raise HTTPException(status_code=404, detail="Anticipo no encontrado")
    gestor_carga = repositories.get_gestor_carga_by_id(db, orden_carga.gestor_carga_id)
    if not gestor_carga:
        raise HTTPException(status_code=404, detail="Anticipo no encontrado")
    usuario = repositories.get_by_username(db, obj.created_by)
    usuario_nombre = (
        f"{usuario.first_name} {usuario.last_name}" if usuario else "Sistema"
    )
    OUTPUT_FILENAME = f"anticipo_{id}.pdf"
    TEMPLATE_FILENAME = "pdf_anticipo.html"
    template: Template = templateEnv.get_template(TEMPLATE_FILENAME)
    data = {
        "id": id,
        "orden_carga_id": orden_carga.id,
        "flete_id": orden_carga.flete_id,
        "gestor_carga_logo": gestor_carga.logo,
        "gestor_carga_nombre": gestor_carga.nombre,
        "gestor_carga_direccion": gestor_carga.direccion,
        "anticipo_fecha": obj.created_at.strftime("%Y-%m-%d / %H:%M:%S"),
        "anticipo_usuario": usuario_nombre,
        "propietario_nombre": orden_carga.camion_propietario_nombre,
        "chofer_nombre": orden_carga.camion_chofer_nombre,
        "chofer_numero_documento": orden_carga.camion_chofer_numero_documento,
        "chofer_telefono": orden_carga.camion.chofer.telefono,
        "camion_placa": orden_carga.camion_placa,
        "proveedor_nombre": obj.proveedor_nombre,
        "proveedor_numero_documento": obj.punto_venta.proveedor.numero_documento,
        "proveedor_direccion": obj.punto_venta.proveedor.direccion,
        "insumo_descripcion": obj.insumo_descripcion
        if obj.insumo_descripcion
        else "Viático",
        "insumo_precio": obj.insumo_precio if obj.insumo_precio else 1,
        "insumo_unidad": obj.insumo_unidad_abreviatura
        if obj.insumo_unidad_abreviatura
        else "",
        "monto": "{:,.2f}".format(obj.monto_retirado)
        .replace(".", "#")
        .replace(",", ".")
        .replace("#", ","),
        "unidad": obj.unidad_abreviatura if obj.unidad_abreviatura else "",
    }
    source_html = template.render(logo=LOGO_IMAGE_URL, times=range(2), **data)
    pdf_filename = os.path.join(REPORTS_FOLDER, OUTPUT_FILENAME)
    from_string(source_html, pdf_filename)
    return OUTPUT_FILENAME
