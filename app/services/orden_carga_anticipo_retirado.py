from datetime import datetime
import os
from decimal import Decimal
from typing import List, Optional, cast

from app.enums.estado import EstadoEnum
from fastapi import HTTPException
from jinja2 import Template
from pdfkit import from_string  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, logger
from app.config import LOGO_IMAGE_URL, REPORTS_FOLDER, templateEnv, STATICS_FOLDER, dir_path
from app.enums import TipoAnticipoEnum, TipoInsumoEnum
from app.models import Camion, OrdenCargaAnticipoRetirado, TipoAnticipo, TipoInsumo
from app.models.orden_carga import OrdenCarga
from app.models.orden_carga_anticipo_saldo import OrdenCargaAnticipoSaldo
from app.schemas.rounded_decimal_model import RoundedDecimal
from app.utils import number_format

from .camion import update_camion_anticipo_retirado
from .movimiento import create_movimiento_by_anticipo
from .orden_carga_anticipo_porcentaje_create import (
    get_orden_carga_anticipo_porcentaje_by,
)
from .orden_carga_anticipo_saldo import update_orden_carga_anticipo_saldo_by_form
from .orden_carga import validar_habilitacion_para_anticipos
from .user import get_user_by_username
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import HTTPException, status as http_status


def get_orden_carga_anticipo_retirado_list(
    db: Session, gestor_carga_id: Optional[int]
) -> List[OrdenCargaAnticipoRetirado]:
    if gestor_carga_id:
        return repositories.get_orden_carga_anticipo_retirado_list_by_gestor_carga_id(db, gestor_carga_id)
    return repositories.get_orden_carga_anticipo_retirado_list(db)


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


def get_orden_carga_anticipo_saldo_actual(
    db: Session,
    flete_anticipo_id: int,
    orden_carga_id: int,
) -> OrdenCargaAnticipoSaldo:
    saldo = (
        db.query(OrdenCargaAnticipoSaldo)
        .filter(
            OrdenCargaAnticipoSaldo.flete_anticipo_id == flete_anticipo_id,
            OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id,
        )
        .first()
    )
    if saldo is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró saldo para el anticipo especificado."
        )
    return saldo


def create_orden_carga_anticipo_retirado(
    db: Session,
    data: schemas.OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> schemas.OrdenCargaAnticipoRetirado:
    orden_carga = db.query(OrdenCarga).filter(OrdenCarga.id == data.orden_carga_id).first()
    if not orden_carga:
        raise HTTPException(status_code=404, detail="Orden de carga no encontrada")

    chofer_id = orden_carga.chofer_id
    propietario_id = orden_carga.propietario_id
    combinacion_id = orden_carga.combinacion_id

    validar_habilitacion_para_anticipos(db, chofer_id, propietario_id, combinacion_id)

    if data.es_con_litro and data.cantidad_retirada and data.precio_unitario:
        if data.monto_retirado is None:
            data.monto_retirado = RoundedDecimal(
                data.cantidad_retirada * data.precio_unitario
            )

    saldo_actual = get_orden_carga_anticipo_saldo_actual(
        db, data.flete_anticipo_id, data.orden_carga_id
    )

    if saldo_actual is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró saldo para el anticipo especificado."
        )

    nuevo_total_retirado = saldo_actual.total_retirado + data.monto_retirado

    if data.monto_retirado > saldo_actual.saldo:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Ya se retiró el monto del anticipo. Actualice la página para ver el saldo actualizado."
        )

    porcentaje_anticipo = get_orden_carga_anticipo_porcentaje_by(
        db, data.flete_anticipo_id, data.orden_carga_id
    )
    data.orden_carga_anticipo_porcentaje_id = (
        porcentaje_anticipo.id if porcentaje_anticipo else None
    )

    anticipo = repositories.create_orden_cyarga_anticipo_retirado(
        db,
        data,
        modified_by,
    )

    update_orden_carga_anticipo_saldo_by_form(db, data, Decimal(0), modified_by)

    create_movimiento_by_anticipo(
        db, anticipo, anticipo.orden_carga.gestor_carga_id, modified_by
    )

    camion: Camion = anticipo.orden_carga.camion
    update_camion_anticipo_retirado(db, camion)

    return anticipo


# def create_orden_carga_anticipo_retirado(
#     db: Session,
#     data: schemas.OrdenCargaAnticipoRetiradoForm,
#     modified_by: str,
# ) -> schemas.OrdenCargaAnticipoRetirado:
#     if data.es_con_litro and data.cantidad_retirada and data.precio_unitario:
#         if data.monto_retirado is None:
#             data.monto_retirado = RoundedDecimal(
#                 data.cantidad_retirada * data.precio_unitario
#             )

#     # Bloqueo pesimista
#     saldo_obj = (
#         db.query(OrdenCargaAnticipoSaldo)
#         .filter(
#             OrdenCargaAnticipoSaldo.flete_anticipo_id == data.flete_anticipo_id,
#             OrdenCargaAnticipoSaldo.orden_carga_id == data.orden_carga_id,
#         )
#         .with_for_update()
#         .first()
#     )
#     if not saldo_obj:
#         raise HTTPException(status_code=404, detail="Anticipo no encontrado")

#     nuevo_total_retirado = (saldo_obj.total_retirado or 0) + data.monto_retirado
#     nuevo_saldo = (saldo_obj.total_disponible or 0) - nuevo_total_retirado

#     if nuevo_saldo < 0:
#         raise HTTPException(
#             status_code=400,
#             detail="Saldo insuficiente para realizar el retiro.",
#         )

#     saldo_obj.total_retirado = nuevo_total_retirado
#     saldo_obj.saldo = nuevo_saldo
#     saldo_obj.modified_by = modified_by

#     porcentaje_anticipo = get_orden_carga_anticipo_porcentaje_by(
#         db, data.flete_anticipo_id, data.orden_carga_id
#     )
#     data.orden_carga_anticipo_porcentaje_id = (
#         porcentaje_anticipo.id if porcentaje_anticipo else None
#     )

#     anticipo = repositories.create_orden_carga_anticipo_retirado(
#         db,
#         data,
#         modified_by,
#     )
#     create_movimiento_by_anticipo(
#         db, anticipo, anticipo.orden_carga.gestor_carga_id, modified_by
#     )

#     camion: Camion = anticipo.orden_carga.camion
#     update_camion_anticipo_retirado(db, camion)

#     return anticipo


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
    # Obtener la instancia actual
    to_edit_obj = get_orden_carga_anticipo_retirado_by_id(db, id)

    # Validar habilitación para anticipos
    orden_carga = to_edit_obj.orden_carga
    validar_habilitacion_para_anticipos(
        db,
        chofer_id=orden_carga.chofer_id,
        propietario_id=orden_carga.propietario_id,
        combinacion_id=orden_carga.combinacion_id,
    )

    # Calcular monto si es con litro
    if data.es_con_litro and data.cantidad_retirada and data.precio_unitario:
        data.monto_retirado = RoundedDecimal(
            data.cantidad_retirada * data.precio_unitario
        )

    # Actualizar saldo y camion
    update_orden_carga_anticipo_saldo_by_form(
        db, data, to_edit_obj.monto_retirado, modified_by
    )
    camion: Camion = orden_carga.camion
    update_camion_anticipo_retirado(db, camion)

    # Editar y retornar
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


def change_anticipo_status(
    db: Session, id: int, status: EstadoEnum, modified_by: str
) -> schemas.OrdenCargaAnticipoRetirado:
    co = repositories.get_anticipo_by_id(db, id)

    if not co:
        raise HTTPException(status_code=404, detail="OrdenCargaAnticipoRetirado no encontrada")

    movimientos = repositories.get_movimiento_by_anticipo_id(db, co.id)

    # No permitir anular si algún movimiento tiene liquidacion_id distinto de None
    if movimientos:
        for movimiento in movimientos:
            if movimiento.liquidacion_id is not None:
                raise HTTPException(
                    status_code=400,
                    detail="No se puede anular el anticipo porque se encuentra en una liquidación"
                )

    co = repositories.change_anticipo_status(co, db, status, modified_by)

    if movimientos:
        for movimiento in movimientos:
            movimiento.estado = status.value
            movimiento.modified_by = modified_by
            movimiento.modified_at = datetime.now()

            db.commit()
            db.refresh(movimiento)

        saldo = repositories.get_saldo_by_flete_anticipo_id_and_orden_carga_id(
            db, co.flete_anticipo_id, co.orden_carga_id
        )

        if saldo:
            saldo.total_retirado -= co.monto_mon_local
            saldo.saldo += co.monto_mon_local

            db.commit()
            db.refresh(saldo)

        camion = repositories.get_camion_by_orden_carga_id(db, co.orden_carga_id)

        if camion and camion.limite_monto_anticipos is not None:
            camion.total_anticipos_retirados_en_estado_pendiente_o_en_proceso -= co.monto_mon_local
            camion.modified_by = modified_by
            camion.modified_at = datetime.now()

            db.commit()
            db.refresh(camion)

    return co


def get_orden_carga_anticipo_retirado_pdf_by_id(db: Session, id: int) -> str:
    #try:
    logger.info('Inicio del proceso de generación de PDF')

    # Obtención del objeto de anticipo
    obj = repositories.get_orden_carga_anticipo_retirado_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Anticipo no encontrado")

    # Obtención de la orden de carga
    orden_carga = repositories.get_orden_carga_by_id(db, obj.orden_carga_id)
    if not orden_carga:
        raise HTTPException(status_code=404, detail="Orden de carga no encontrada")

    # Obtención del gestor de carga
    gestor_carga = repositories.get_gestor_carga_by_id(db, orden_carga.gestor_carga_id)
    if not gestor_carga:
        raise HTTPException(status_code=404, detail="Gestor de carga no encontrado")

    # Obtención del usuario
    usuario = get_user_by_username(db, obj.created_by)
    usuario_nombre = f"{usuario.first_name} {usuario.last_name}" if usuario else "Sistema"
    OUTPUT_FILENAME = f"anticipo_{id}.pdf"

    # Datos para el PDF
    data = {
        "id": id,
        "orden_carga_id": orden_carga.id,
        "flete_id": orden_carga.flete_id,
        "gestor_carga_logo": gestor_carga.logo,
        "gestor_carga_nombre": gestor_carga.nombre,
        "gestor_carga_documento": gestor_carga.numero_documento,
        "gestor_carga_direccion": gestor_carga.direccion,
        "anticipo_fecha": obj.created_at.strftime("%Y-%m-%d / %H:%M:%S"),
        "anticipo_usuario": usuario_nombre,
        "propietario_nombre": orden_carga.camion_propietario_nombre,
        "propietario_documento": orden_carga.camion_propietario_documento,
        "chofer_nombre": orden_carga.combinacion.chofer_nombre,
        "chofer_numero_documento": orden_carga.combinacion.chofer_numero_documento,
        "camion_placa": orden_carga.camion_placa,
        "camion_marca": orden_carga.camion_marca,
        "camion_color": orden_carga.camion_color,
        "proveedor_nombre": obj.proveedor_nombre,
        "proveedor_pdv_nombre": obj.punto_venta.nombre_corto,
        "proveedor_numero_documento": obj.punto_venta.proveedor.numero_documento,
        "proveedor_direccion": obj.punto_venta.proveedor.direccion,
        "concepto": obj.concepto,
        "insumo_descripcion": obj.insumo_descripcion or "Viático",
        "insumo_precio": number_format(obj.insumo_precio) if obj.insumo_precio else 1,
        "insumo_unidad": obj.insumo_unidad_abreviatura or "",
        "cantidad_retirada": number_format(obj.cantidad_retirada) if obj.cantidad_retirada else 1,
        "monto": number_format(obj.monto_retirado),
        "unidad": obj.unidad_abreviatura or "",
        "observacion": obj.observacion or "",
    }

    # Renderizado del template
    template: Template = templateEnv.get_template("pdf_anticipo.html")
    STATICS_FOLDER_lOGO = os.path.join(dir_path, "statics/logo-icargo.png")
    source_html = template.render(logo=STATICS_FOLDER_lOGO, times=range(2), **data)
    logger.info(f'LOGO_IMAGE_URL: {STATICS_FOLDER_lOGO}')
    logger.info('html generado exitosamente')
    logger.info(f'html: {source_html}')
    # Generación del PDF
    pdf_filename = os.path.join(REPORTS_FOLDER, OUTPUT_FILENAME)
    from_string(source_html, pdf_filename, {"enable-local-file-access": "", "page-size": "Legal"})
    logger.info('PDF generado exitosamente')
    #return HTMLResponse(content=source_html, status_code=200)
    return OUTPUT_FILENAME
    #except Exception as e:
    #    logger.error(f'Error al generar el PDF: {e}')
    #    raise HTTPException(status_code=500, detail="Error al generar el PDF")
