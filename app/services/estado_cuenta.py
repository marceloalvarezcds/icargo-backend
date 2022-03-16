import os
from typing import List, Optional

from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.config import REPORTS_FOLDER
from app.schemas import EstadoCuenta


def get_estado_cuenta_list(
    db: Session, gestor_carga_id: Optional[int] = None
) -> List[EstadoCuenta]:
    if gestor_carga_id:
        results = repositories.get_estado_cuenta_list_by_gestor_carga_id(
            db, gestor_carga_id
        )
    else:
        results = repositories.get_estado_cuenta_list(db)
    return EstadoCuenta.result_of_query_to_list(results)


def get_estado_cuenta_reports(db: Session) -> str:
    datalist = get_estado_cuenta_list(db)
    wb = Workbook()
    ws = wb.active

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "Tipo de Contraparte"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Nombre Contraparte"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "Nº Contraparte"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "Pendiente"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "En Proceso"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=6)
    title_cell.value = "Confirmado"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Finalizado"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.tipo_contraparte_descripcion

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.contraparte

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.contraparte_numero_documento

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.pendiente

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.en_proceso

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.confirmado

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = item.finalizado

    ws.auto_filter.ref = ws.dimensions
    filename = "estado_cuenta_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
