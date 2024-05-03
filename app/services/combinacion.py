import asyncio
import os
from typing import List, Optional

from app.config import REPORTS_FOLDER
from fastapi import HTTPException # type: ignore
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app.models import Combinacion
from app import repositories, schemas
from .semi import get_semi_by_id


def get_combinacion_by_id(db: Session, id: int) -> Combinacion:
    obj = repositories.get_combinacion_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Combinacion no encontrada")
    return obj


def get_combinacion_by_gestor_cuenta_and_combinacion_id(
    db: Session, semi_id: int, gestor_cuenta_id: Optional[int]
) -> List[Combinacion]:
    semi = get_semi_by_id(db, semi_id)
    lista = repositories.get_propietario_list_by_gestor_cuenta_id(db, gestor_cuenta_id)
    if semi.propietario:
        combinacion: Combinacion = semi.combinacion
        lista.append(combinacion)
    return lista


async def create_combinacion(
    db: Session,
    data: schemas.CombinacionCreateModel,
    modified_by: str
) -> schemas.Combinacion:
    # Verificar si existen los propietarios, camiones, choferes y semirremolques
    propietario_exists = (repositories.get_propietario_by_id(db, data.propietario_id))
    camion_exists = (repositories.get_camion_by_id(db, data.camion_id))
    chofer_exists = (repositories.get_chofer_by_id(db, data.chofer_id))
    semi_exists = (repositories.get_chofer_by_id(db, data.semi_id))

    # Si no existen alguno de los elementos, levanta una excepción
    if not propietario_exists:
        raise HTTPException(
            status_code=404,
            detail="El propietario especificado no existe."
        )
    if not camion_exists:
        raise HTTPException(
            status_code=404,
            detail="El camión especificado no existe."
        )
    if not chofer_exists:
        raise HTTPException(
            status_code=404,
            detail="El chofer especificado no existe."
        )
    if not semi_exists:
        raise HTTPException(
            status_code=404,
            detail="El semirremolque especificado no existe."
        )

    # Si todos los elementos existen, procede a crear la combinación
    combinacion = repositories.create_combinacion(
        db,
        data,
        modified_by,
    )

    return combinacion

async def edit_combinacion(
    id: int,
    db: Session,
    data: schemas.CombinacionCreateModel,
    modified_by: str,
) -> schemas.Combinacion:
    # Obtener la combinación existente de la base de datos
    combinacion = repositories.get_combinacion_by_id(db, id)
    if not combinacion:
        # Manejar el caso en que la combinación no exista
        raise HTTPException(status_code=404, detail="Combinación no encontrada")

    # Verificar si existe el propietario
    if data.propietario_id is not None:
        propietario = repositories.get_propietario_by_id(db, data.propietario_id)
        if not propietario:
            raise HTTPException(status_code=404, detail="Propietario no encontrado")

    # Verificar si existe el chofer
    if data.chofer_id is not None:
        chofer = repositories.get_chofer_by_id(db, data.chofer_id)
        if not chofer:
            raise HTTPException(status_code=404, detail="Chofer no encontrado")

    # Verificar si existe el camion
    if data.camion_id is not None:
        camion = repositories.get_camion_by_id(db, data.camion_id)
        if not camion:
            raise HTTPException(status_code=404, detail="Camión no encontrado")

    # Verificar si existe el semi
    if data.semi_id is not None:
        semi = repositories.get_semi_by_id(db, data.semi_id)
        if not semi:
            raise HTTPException(status_code=404, detail="Semi no encontrado")

    # Actualizar los campos de la combinación con los datos proporcionados
    if data.propietario_id is not None:
        combinacion.propietario_id = data.propietario_id
    if data.camion_id is not None:
        combinacion.camion_id = data.camion_id
    if data.chofer_id is not None:
        combinacion.chofer_id = data.chofer_id
    if data.semi_id is not None:
        combinacion.semi_id = data.semi_id
    if data.comentario is not None:
        combinacion.comentario = data.comentario
    if data.capacidad_total_combinacion is not None:
        combinacion.capacidad_total_combinacion = data.capacidad_total_combinacion
    # Actualizar otros campos según sea necesario

    # Guardar los cambios en la base de datos
    db.add(combinacion)
    db.commit()
    db.refresh(combinacion)

    return combinacion


def get_combinacion_reports(db: Session) -> str:
    datalist = repositories.get_combinacion_list(db)
    wb = Workbook()
    # get worksheet
    ws = wb.active
    

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Estado"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Comentario"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=8)
    title_cell.value = "Capacidad Total Combinación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=9)
    title_cell.value = "Usuario creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=10)
    title_cell.value = "Fecha creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=11)
    title_cell.value = "Usuario modificación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=12)
    title_cell.value = "Fecha modificación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.estado

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.comentario

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.capacidad_total_combinacion

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.created_by

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.created_at

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = item.modified_by

        value_cell = ws.cell(row=row + 2, column=8)
        value_cell.value = item.modified_at

    ws.auto_filter.ref = ws.dimensions
    filename = "combinacion_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
