from typing import Optional

from fastapi import HTTPException, UploadFile  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.enums.estado import EstadoEnum
from app.models import Chofer
from app.schemas import ChoferForm, Propietario

from .gestor_carga_propietario import (
    create_gestor_carga_propietario,
    edit_gestor_carga_propietario,
)
from .propietario import get_propietario_detail
from .propietario_check_files import check_files, get_propietario_by_ruc


async def create_or_edit_propietario_by_chofer(
    db: Session,
    data: ChoferForm,
    foto_documento_frente_file: Optional[UploadFile],
    foto_documento_reverso_file: Optional[UploadFile],
    foto_perfil_url: Optional[str],
    gestor_cuenta_id: Optional[int],
    chofer: Chofer,
    modified_by: str,
) -> Optional[Propietario]:
    if not data.ruc:
        raise HTTPException(
            status_code=409,
            detail="El ruc es requerido para crear el Propietario",
        )
    (foto_documento_frente_url, foto_documento_reverso_url, _,) = await check_files(
        foto_documento_frente_file,
        foto_documento_reverso_file,
        None,
    )
    exists = get_propietario_by_ruc(db, data.ruc)
    if exists:
        obj = repositories.edit_propietario_by_chofer(
            exists,
            db,
            data,
            foto_documento_frente_url,
            foto_documento_reverso_url,
            foto_perfil_url,
            chofer,
            modified_by,
        )
        edit_gestor_carga_propietario(
            db, obj, gestor_cuenta_id, data.alias, modified_by
        )
    else:
        obj = repositories.create_propietario_by_chofer(
            db,
            data,
            gestor_cuenta_id,
            foto_documento_frente_url,
            foto_documento_reverso_url,
            foto_perfil_url,
            chofer,
            modified_by,
        )
        create_gestor_carga_propietario(
            db, obj, gestor_cuenta_id, data.alias, modified_by
        )
    return get_propietario_detail(db, obj, gestor_cuenta_id)


def disable_propietario_by_ruc(
    db: Session,
    propietario_ruc: Optional[str],
    modified_by: str,
):
    if propietario_ruc:
        propietario = get_propietario_by_ruc(db, propietario_ruc)
        if propietario:
            repositories.change_propietario_status(
                propietario, db, EstadoEnum.INACTIVO, modified_by
            )
