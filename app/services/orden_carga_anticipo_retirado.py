import os
from decimal import Decimal
from typing import cast

from fastapi import HTTPException
from jinja2 import Template
from pdfkit import from_string  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.config import LOGO_IMAGE_URL, REPORTS_FOLDER, templateEnv
from app.enums import TipoAnticipoEnum, TipoInsumoEnum
from app.models import OrdenCargaAnticipoRetirado, TipoAnticipo, TipoInsumo
from app.schemas.rounded_decimal_model import RoundedDecimal
from app.utils import number_format

from .movimiento import create_movimiento_by_anticipo
from .orden_carga_anticipo_saldo import update_orden_carga_anticipo_saldo_by_form


def get_tipo_anticipo_by_id(db: Session, id: int) -> TipoAnticipo:
    obj = repositories.get_tipo_anticipo_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Tipo de Anticipo no encontrado")
    return obj


def get_tipo_insumo_by_id(db: Session, id: int) -> TipoInsumo:
    obj = repositories.get_tipo_insumo_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Tipo de Insumo no encontrado")
    return obj


def get_error_message(db: Session, data: schemas.OrdenCargaAnticipoRetiradoForm) -> str:
    if data.numero_comprobante:
        return f"El Anticipo con comporbante {data.numero_comprobante} ya existe"
    else:
        tipo_anticipo = get_tipo_anticipo_by_id(db, data.tipo_anticipo_id)
        if tipo_anticipo.descripcion == TipoAnticipoEnum.EFECTIVO.value:
            return "Ya existe anticipo de Efectivo para esta OC"
        else:
            tipo_insumo = get_tipo_insumo_by_id(db, cast(int, data.tipo_insumo_id))
            if tipo_insumo.descripcion == TipoInsumoEnum.COMBUSTIBLE.value:
                return "Ya existe anticipo de Combustible para esta OC en este Punto de Venta"
            else:
                return "Ya existe anticipo de Lubricante para esta OC en este Punto de Venta"


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
            detail=get_error_message(db, data),
        )
    if data.es_con_litro and data.cantidad_retirada and data.precio_unitario:
        data.monto_retirado = RoundedDecimal(
            data.cantidad_retirada * data.precio_unitario
        )
    update_orden_carga_anticipo_saldo_by_form(db, data, Decimal(0), modified_by)
    anticipo = repositories.create_orden_carga_anticipo_retirado(
        db,
        data,
        modified_by,
    )
    create_movimiento_by_anticipo(
        db, anticipo, anticipo.orden_carga.gestor_carga_id, modified_by
    )
    return anticipo


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
            detail=get_error_message(db, data),
        )
    if data.es_con_litro and data.cantidad_retirada and data.precio_unitario:
        data.monto_retirado = RoundedDecimal(
            data.cantidad_retirada * data.precio_unitario
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
        "insumo_precio": number_format(obj.insumo_precio) if obj.insumo_precio else 1,
        "insumo_unidad": obj.insumo_unidad_abreviatura
        if obj.insumo_unidad_abreviatura
        else "",
        "monto": number_format(obj.monto_retirado),
        "unidad": obj.unidad_abreviatura if obj.unidad_abreviatura else "",
    }
    source_html = template.render(logo=LOGO_IMAGE_URL, times=range(2), **data)
    pdf_filename = os.path.join(REPORTS_FOLDER, OUTPUT_FILENAME)
    from_string(source_html, pdf_filename, {"page-size": "Legal"})
    return OUTPUT_FILENAME
