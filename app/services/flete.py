import os
from typing import Optional

from fastapi import HTTPException
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.config import REPORTS_FOLDER
from app.enums import EstadoEnum
from app.models import Flete
from app.utils.meta_inspect import get_dict

from .flete_anticipo import update_flete_anticipo_list
from .flete_complemento import update_flete_complemento_list
from .flete_descuento import update_flete_descuento_list
from .flete_destinatario import (
    get_destinatario_selected_list_by_flete,
    update_flete_destinatario_list,
)


def get_flete_detail(model: Flete) -> schemas.Flete:
    obj_dict = get_dict(model, ignore_keys=["flete"], for_json=False)
    obj_dict["destinatarios"] = get_destinatario_selected_list_by_flete(model)
    return schemas.Flete.parse_obj(obj_dict)


def create_flete(
    db: Session,
    data: schemas.FleteForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> schemas.Flete:
    obj = repositories.create_flete(
        db,
        data,
        gestor_carga_id,
        modified_by,
    )
    update_flete_anticipo_list(db, data.anticipos, obj, modified_by)
    update_flete_complemento_list(db, data.complementos, obj, modified_by)
    update_flete_descuento_list(db, data.descuentos, obj, modified_by)
    update_flete_destinatario_list(db, data.destinatarios, obj, modified_by)
    return get_flete_detail(obj)


def get_flete_by_id(db: Session, id: int) -> Flete:
    obj = repositories.get_flete_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Flete no encontrado")
    return obj


def get_flete_detail_by_id(db: Session, id: int) -> schemas.Flete:
    return get_flete_detail(get_flete_by_id(db, id))


def edit_flete(
    id: int,
    db: Session,
    data: schemas.FleteForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> schemas.Flete:
    to_edit_obj = get_flete_by_id(db, id)
    obj = repositories.edit_flete(
        to_edit_obj,
        db,
        data,
        gestor_carga_id,
        modified_by,
    )
    update_flete_anticipo_list(db, data.anticipos, obj, modified_by)
    update_flete_complemento_list(db, data.complementos, obj, modified_by)
    update_flete_descuento_list(db, data.descuentos, obj, modified_by)
    update_flete_destinatario_list(db, data.destinatarios, obj, modified_by)
    return get_flete_detail(obj)


def delete_flete(db: Session, id: int, modified_by: str) -> schemas.Flete:
    co = get_flete_by_id(db, id)
    co.publicado = False
    return get_flete_detail(repositories.delete_flete(co, db, modified_by))


def change_flete_status(
    db: Session, id: int, status: EstadoEnum, modified_by: str
) -> schemas.Flete:
    co = get_flete_by_id(db, id)
    co.publicado = False
    return get_flete_detail(
        repositories.change_flete_status(co, db, status, modified_by)
    )


def change_flete_public_status(
    db: Session, id: int, is_public: bool, modified_by: str
) -> schemas.Flete:
    co = get_flete_by_id(db, id)
    if is_public and co.estado == EstadoEnum.CANCELADO.value:
        raise HTTPException(
            status_code=403,
            detail="El Flete ya está cancelado, no puede publicarlo",
        )
    return get_flete_detail(
        repositories.change_flete_public_status(co, db, is_public, modified_by)
    )


def get_flete_reports(db: Session) -> str:
    datalist = repositories.get_flete_list(db)
    wb = Workbook()
    # get worksheet
    ws = wb.active

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "Nº"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Remitente"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "Producto"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "Tipo de Carga"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "Número de Lote"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=6)
    title_cell.value = "Publicado"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Tipo de Pedido"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=8)
    title_cell.value = "Estado"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=9)
    title_cell.value = "Gestor de Cuenta"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=10)
    title_cell.value = "Origen"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=11)
    title_cell.value = "Origen Indicaciones"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=12)
    title_cell.value = "Destino"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=13)
    title_cell.value = "Destino Indicaciones"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=14)
    title_cell.value = "Distancia"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=15)
    title_cell.value = "Tipo de flete"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=16)
    title_cell.value = "Cantidad a Transportar"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=17)
    title_cell.value = "Condición para Gestor - Moneda"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=18)
    title_cell.value = "Condición para Gestor - Tarifa"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=19)
    title_cell.value = "Condición para Gestor - Unidad"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=20)
    title_cell.value = "Condición para Propietario - Moneda"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=21)
    title_cell.value = "Condición para Propietario - Tarifa"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=22)
    title_cell.value = "Condición para Propietario - Unidad"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=23)
    title_cell.value = "Merma para Gestor - Valor"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=24)
    title_cell.value = "Merma para Gestor - Moneda"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=25)
    title_cell.value = "Merma para Gestor - Unidad"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=26)
    title_cell.value = "Merma para Gestor - Es Cálculo porcentual"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=27)
    title_cell.value = "Merma para Gestor - Tolerancia"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=28)
    title_cell.value = "Merma para Propietario - Valor"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=29)
    title_cell.value = "Merma para Propietario - Moneda"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=30)
    title_cell.value = "Merma para Propietario - Unidad"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=31)
    title_cell.value = "Merma para Propietario - Es Cálculo porcentual"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=32)
    title_cell.value = "Merma para Propietario - Tolerancia"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=33)
    title_cell.value = "Vigencia de Anticipos"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=34)
    title_cell.value = "Usuario creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=35)
    title_cell.value = "Fecha creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=36)
    title_cell.value = "Usuario modificación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=37)
    title_cell.value = "Fecha modificación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.id

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.remitente_nombre

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.producto_descripcion

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.tipo_carga_descripcion

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.numero_lote

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.publicado_descripcion

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = "Subasta" if item.es_subasta else "Flete"

        value_cell = ws.cell(row=row + 2, column=8)
        value_cell.value = item.estado

        value_cell = ws.cell(row=row + 2, column=9)
        value_cell.value = item.gestor_cuenta_nombre

        value_cell = ws.cell(row=row + 2, column=10)
        value_cell.value = item.origen_nombre

        value_cell = ws.cell(row=row + 2, column=11)
        value_cell.value = item.origen_indicacion

        value_cell = ws.cell(row=row + 2, column=12)
        value_cell.value = item.destino_nombre

        value_cell = ws.cell(row=row + 2, column=13)
        value_cell.value = item.destino_indicacion

        value_cell = ws.cell(row=row + 2, column=14)
        value_cell.value = item.distancia

        value_cell = ws.cell(row=row + 2, column=15)
        value_cell.value = item.tipo_flete.value

        value_cell = ws.cell(row=row + 2, column=16)
        value_cell.value = item.condicion_cantidad

        value_cell = ws.cell(row=row + 2, column=17)
        value_cell.value = item.condicion_gestor_cuenta_moneda_nombre

        value_cell = ws.cell(row=row + 2, column=18)
        value_cell.value = item.condicion_gestor_cuenta_tarifa

        value_cell = ws.cell(row=row + 2, column=19)
        value_cell.value = item.condicion_gestor_cuenta_unidad_descripcion

        value_cell = ws.cell(row=row + 2, column=20)
        value_cell.value = item.condicion_propietario_moneda_nombre

        value_cell = ws.cell(row=row + 2, column=21)
        value_cell.value = item.condicion_propietario_tarifa

        value_cell = ws.cell(row=row + 2, column=22)
        value_cell.value = item.condicion_propietario_unidad_descripcion

        value_cell = ws.cell(row=row + 2, column=23)
        value_cell.value = item.merma_gestor_cuenta_valor

        value_cell = ws.cell(row=row + 2, column=24)
        value_cell.value = item.merma_gestor_cuenta_moneda_nombre

        value_cell = ws.cell(row=row + 2, column=25)
        value_cell.value = item.merma_gestor_cuenta_unidad_descripcion

        value_cell = ws.cell(row=row + 2, column=26)
        value_cell.value = "Si" if item.merma_gestor_cuenta_es_porcentual else "No"

        value_cell = ws.cell(row=row + 2, column=27)
        value_cell.value = item.merma_gestor_cuenta_tolerancia

        value_cell = ws.cell(row=row + 2, column=28)
        value_cell.value = item.merma_propietario_valor

        value_cell = ws.cell(row=row + 2, column=29)
        value_cell.value = item.merma_propietario_moneda_nombre

        value_cell = ws.cell(row=row + 2, column=30)
        value_cell.value = item.merma_propietario_unidad_descripcion

        value_cell = ws.cell(row=row + 2, column=31)
        value_cell.value = "Si" if item.merma_propietario_es_porcentual else "No"

        value_cell = ws.cell(row=row + 2, column=32)
        value_cell.value = item.merma_propietario_tolerancia

        value_cell = ws.cell(row=row + 2, column=33)
        value_cell.value = item.vigencia_anticipos

        value_cell = ws.cell(row=row + 2, column=34)
        value_cell.value = item.created_by

        value_cell = ws.cell(row=row + 2, column=35)
        value_cell.value = item.created_at

        value_cell = ws.cell(row=row + 2, column=36)
        value_cell.value = item.modified_by

        value_cell = ws.cell(row=row + 2, column=37)
        value_cell.value = item.modified_at

    ws.auto_filter.ref = ws.dimensions
    filename = "flete_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
