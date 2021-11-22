import os
from typing import List, Optional

from fastapi import HTTPException, UploadFile  # type: ignore
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.config import REPORTS_FOLDER
from app.models import (
    GestorCargaPropietario,
    Propietario,
    PropietarioContactoGestorCarga,
)

from .gestor_carga_propietario import (
    create_gestor_carga_propietario,
    edit_gestor_carga_propietario,
)
from .pictshare import upload_and_get_image_url
from .propietario_contacto import update_propietario_contacto_list


def get_propietario_detail(
    obj: Propietario, gestor_cuenta_id: Optional[int]
) -> schemas.Propietario:
    obj_dict = obj.as_dict(for_json=False)
    contactos: List[PropietarioContactoGestorCarga] = obj.contactos
    ges: List[GestorCargaPropietario] = obj.gestores
    gestores = [x for x in ges if x.gestor_carga_id == gestor_cuenta_id]
    obj_dict["contactos"] = [
        x for x in contactos if x.gestor_carga_id == gestor_cuenta_id
    ]
    obj_dict["gestor_carga_propietario"] = gestores[0] if len(gestores) > 0 else None
    obj_dict["tipo_persona"] = obj.tipo_persona
    obj_dict["gestor_cuenta_nombre"] = (
        obj.gestor_cuenta.nombre if obj.gestor_cuenta else None
    )
    obj_dict[
        "oficial_cuenta_nombre"
    ] = f"{obj.oficial_cuenta.first_name} {obj.oficial_cuenta.last_name}"
    obj_dict["pais_origen"] = obj.pais_origen
    obj_dict["ciudad"] = obj.ciudad
    return schemas.Propietario.parse_obj(obj_dict)


async def create_propietario(
    db: Session,
    data: schemas.PropietarioForm,
    foto_documento_file: UploadFile,
    foto_perfil_file: UploadFile,
    gestor_cuenta_id: Optional[int],
    modified_by: str,
) -> schemas.Propietario:
    if repositories.get_propietario_by(db, data.tipo_persona_id, data.ruc):
        raise HTTPException(
            status_code=409,
            detail=f"El Propietario con documento {data.ruc} ya existe",
        )
    foto_documento_url = await upload_and_get_image_url(foto_documento_file)
    foto_perfil_url = await upload_and_get_image_url(foto_perfil_file)
    obj = repositories.create_propietario(
        db, data, gestor_cuenta_id, foto_documento_url, foto_perfil_url, modified_by
    )
    update_propietario_contacto_list(
        db, data.contactos, obj, gestor_cuenta_id, modified_by
    )
    create_gestor_carga_propietario(db, obj, gestor_cuenta_id, data.alias, modified_by)
    return get_propietario_detail(obj, gestor_cuenta_id)


def get_propietario_by_id(db: Session, id: int) -> Propietario:
    obj = repositories.get_propietario_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return obj


def get_propietario_by_id_and_gestor_cuenta_id(
    db: Session, id: int, gestor_cuenta_id: Optional[int] = None
) -> schemas.Propietario:
    obj = repositories.get_propietario_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return get_propietario_detail(obj, gestor_cuenta_id)


async def edit_propietario(
    id: int,
    db: Session,
    data: schemas.PropietarioForm,
    foto_documento_file: Optional[UploadFile],
    foto_perfil_file: Optional[UploadFile],
    gestor_cuenta_id: Optional[int],
    modified_by: str,
) -> schemas.Propietario:
    exists = repositories.get_propietario_by(db, data.tipo_persona_id, data.ruc)
    if exists and exists.id != id:
        raise HTTPException(
            status_code=409,
            detail=f"El Propietario con documento {data.ruc} ya existe",
        )
    foto_documento_url = (
        await upload_and_get_image_url(foto_documento_file)
        if foto_documento_file
        else None
    )
    foto_perfil_url = (
        await upload_and_get_image_url(foto_perfil_file) if foto_perfil_file else None
    )
    to_edit_obj = get_propietario_by_id(db, id)
    obj = repositories.edit_propietario(
        to_edit_obj, db, data, foto_documento_url, foto_perfil_url, modified_by
    )
    update_propietario_contacto_list(
        db, data.contactos, obj, gestor_cuenta_id, modified_by
    )
    edit_gestor_carga_propietario(db, obj, gestor_cuenta_id, data.alias, modified_by)
    return get_propietario_detail(obj, gestor_cuenta_id)


def delete_propietario(
    db: Session, id: int, gestor_cuenta_id: Optional[int], modified_by: str
) -> schemas.Propietario:
    co = get_propietario_by_id(db, id)
    obj = repositories.delete_propietario(co, db, modified_by)
    return get_propietario_detail(obj, gestor_cuenta_id)


def get_propietario_reports(db: Session) -> str:
    datalist = repositories.get_propietario_list(db)
    wb = Workbook()
    # get worksheet
    ws = wb.active

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "Nombre"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "Tipo de Persona"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "RUC"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "Gestor de Cuenta"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=6)
    title_cell.value = "Oficial de Cuenta"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Dirección"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=8)
    title_cell.value = "Ubicación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.nombre

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.tipo_persona.descripcion

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.ruc

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.gestor_cuenta.nombre if item.gestor_cuenta else ""

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.oficial_cuenta.nombre if item.oficial_cuenta else ""

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = item.direccion if item.direccion else ""

        value_cell = ws.cell(row=row + 2, column=8)
        value_cell.value = f"{item.ciudad.nombre}/{item.ciudad.localidad.nombre}/{item.ciudad.localidad.pais.nombre_corto}"  # noqa

    ws.auto_filter.ref = ws.dimensions
    filename = "propietario_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
