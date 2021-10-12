import os

from fastapi import UploadFile  # type: ignore
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.config import REPORTS_FOLDER
from app.models import CentroOperativo
from app.schemas import CentroOperativoForm

from .pictshare import upload_and_get_image_url


async def create_centro_operativo(
    db: Session,
    data: Json[CentroOperativoForm],  # type: ignore
    file: UploadFile,
    modified_by: str,
) -> CentroOperativo:
    logo_url = await upload_and_get_image_url(file)
    return repositories.create_centro_operativo(db, data, logo_url, modified_by)


def get_centro_operativo_reports(db: Session) -> str:
    datalist = repositories.get_centro_operativo_list(db)
    wb = Workbook()
    # get worksheet
    ws = wb.active
    # title = f"Lista de Centros Operativos"
    # title_cell = ws.cell(row=1, column=1)
    # title_cell.font = Font(size=12, bold=True)
    # title_cell.value = title.upper()

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "Nombre"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Nombre Corto"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "Dirección"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "Ubicación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "Clasificación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.nombre

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.nombre_corto if item.nombre_corto else ""

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.direccion if item.direccion else ""

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = f"{item.ciudad.nombre}/{item.ciudad.localidad.nombre}/{item.ciudad.localidad.pais.nombre_corto}"  # noqa

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.clasificacion.nombre

    ws.auto_filter.ref = ws.dimensions
    filename = "centro_operativo_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
