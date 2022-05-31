import os
from typing import Optional

from fastapi import HTTPException, UploadFile  # type: ignore
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.config import REPORTS_FOLDER
from app.enums import EstadoEnum
from app.models import Camion

from .camion_check_files import check_files


async def create_camion(
    db: Session,
    data: schemas.CamionForm,
    foto_file: Optional[UploadFile],
    foto_habilitacion_municipal_frente_file: Optional[UploadFile],
    foto_habilitacion_municipal_reverso_file: Optional[UploadFile],
    foto_habilitacion_transporte_frente_file: Optional[UploadFile],
    foto_habilitacion_transporte_reverso_file: Optional[UploadFile],
    foto_habilitacion_automotor_frente_file: Optional[UploadFile],
    foto_habilitacion_automotor_reverso_file: Optional[UploadFile],
    modified_by: str,
) -> schemas.Camion:
    if repositories.get_camion_by(db, data.placa):
        raise HTTPException(
            status_code=409,
            detail=f"El Camión con placa {data.placa} ya existe",
        )
    (
        foto_url,
        foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso_url,
        foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso_url,
        foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso_url,
    ) = await check_files(
        foto_file,
        foto_habilitacion_municipal_frente_file,
        foto_habilitacion_municipal_reverso_file,
        foto_habilitacion_transporte_frente_file,
        foto_habilitacion_transporte_reverso_file,
        foto_habilitacion_automotor_frente_file,
        foto_habilitacion_automotor_reverso_file,
    )
    return repositories.create_camion(
        db,
        data,
        foto_url,
        foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso_url,
        foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso_url,
        foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso_url,
        modified_by,
    )


def get_camion_by_id(db: Session, id: int) -> Camion:
    obj = repositories.get_camion_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Camion no encontrado")
    return obj


async def edit_camion(
    id: int,
    db: Session,
    data: schemas.CamionForm,
    foto_file: Optional[UploadFile],
    foto_habilitacion_municipal_frente_file: Optional[UploadFile],
    foto_habilitacion_municipal_reverso_file: Optional[UploadFile],
    foto_habilitacion_transporte_frente_file: Optional[UploadFile],
    foto_habilitacion_transporte_reverso_file: Optional[UploadFile],
    foto_habilitacion_automotor_frente_file: Optional[UploadFile],
    foto_habilitacion_automotor_reverso_file: Optional[UploadFile],
    modified_by: str,
) -> schemas.Camion:
    if data.placa:
        exists = repositories.get_camion_by(db, data.placa)
        if exists and exists.id != id:
            raise HTTPException(
                status_code=409,
                detail=f"El Camión con placa {data.placa} ya existe",
            )
    (
        foto_url,
        foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso_url,
        foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso_url,
        foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso_url,
    ) = await check_files(
        foto_file,
        foto_habilitacion_municipal_frente_file,
        foto_habilitacion_municipal_reverso_file,
        foto_habilitacion_transporte_frente_file,
        foto_habilitacion_transporte_reverso_file,
        foto_habilitacion_automotor_frente_file,
        foto_habilitacion_automotor_reverso_file,
    )
    to_edit_obj = get_camion_by_id(db, id)
    return repositories.edit_camion(
        to_edit_obj,
        db,
        data,
        foto_url,
        foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso_url,
        foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso_url,
        foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso_url,
        modified_by,
    )


def delete_camion(db: Session, id: int, modified_by: str) -> schemas.Camion:
    co = get_camion_by_id(db, id)
    return repositories.delete_camion(co, db, modified_by)


def change_camion_status(
    db: Session, id: int, status: EstadoEnum, modified_by: str
) -> schemas.Camion:
    co = get_camion_by_id(db, id)
    return repositories.change_camion_status(co, db, status, modified_by)


def get_camion_reports(db: Session) -> str:
    datalist = repositories.get_camion_list(db)
    wb = Workbook()
    # get worksheet
    ws = wb.active

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "Placa"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Nombre del Propietario"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "RUC del Propietario"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "Nombre del Chofer"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "Número de Documento del Chofer"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=6)
    title_cell.value = "Número de Chasís"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Tipo"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=8)
    title_cell.value = "Marca"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=9)
    title_cell.value = "Gestor de Cuenta"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=10)
    title_cell.value = "Oficial de Cuenta"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=11)
    title_cell.value = "Estado"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=12)
    title_cell.value = "Usuario creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=13)
    title_cell.value = "Fecha creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=14)
    title_cell.value = "Usuario modificación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=15)
    title_cell.value = "Fecha modificación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.placa

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.propietario.nombre

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.propietario.ruc

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.chofer_nombre

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.chofer_numero_documento

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.numero_chasis

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = item.tipo_descripcion

        value_cell = ws.cell(row=row + 2, column=8)
        value_cell.value = item.marca_descripcion

        value_cell = ws.cell(row=row + 2, column=9)
        value_cell.value = item.gestor_cuenta_nombre

        value_cell = ws.cell(row=row + 2, column=10)
        value_cell.value = item.oficial_cuenta_nombre

        value_cell = ws.cell(row=row + 2, column=11)
        value_cell.value = item.estado

        value_cell = ws.cell(row=row + 2, column=12)
        value_cell.value = item.created_by

        value_cell = ws.cell(row=row + 2, column=13)
        value_cell.value = item.created_at

        value_cell = ws.cell(row=row + 2, column=14)
        value_cell.value = item.modified_by

        value_cell = ws.cell(row=row + 2, column=15)
        value_cell.value = item.modified_at

    ws.auto_filter.ref = ws.dimensions
    filename = "camion_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
