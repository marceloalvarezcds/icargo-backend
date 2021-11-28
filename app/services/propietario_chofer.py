from typing import Optional

from fastapi import HTTPException, UploadFile  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.schemas import Chofer, PropietarioForm

from .chofer import get_chofer_detail
from .chofer_check_files import check_files
from .gestor_carga_chofer import create_gestor_carga_chofer, edit_gestor_carga_chofer


async def create_or_edit_chofer_by_propietario(
    db: Session,
    data: PropietarioForm,
    foto_documento_frente_file: Optional[UploadFile],
    foto_documento_reverso_file: Optional[UploadFile],
    foto_registro_frente_file: Optional[UploadFile],
    foto_registro_reverso_file: Optional[UploadFile],
    foto_perfil_url: Optional[str],
    gestor_cuenta_id: Optional[int],
    modified_by: str,
    chofer_id: Optional[int] = None,
) -> Optional[Chofer]:
    d = "El pais emisor, tipo y número de documento son requeridos para crear el Chofer"
    if (
        not data.tipo_documento_id
        or not data.pais_emisor_documento_id
        or not data.numero_documento
    ):
        raise HTTPException(
            status_code=409,
            detail=d,
        )
    (
        foto_documento_frente_url,
        foto_documento_reverso_url,
        foto_registro_reverso_url,
        foto_registro_frente_url,
        _,
    ) = await check_files(
        foto_documento_frente_file,
        foto_documento_reverso_file,
        foto_registro_frente_file,
        foto_registro_reverso_file,
        None,
    )
    exists = repositories.get_chofer_by(
        db,
        data.tipo_documento_id,
        data.pais_emisor_documento_id,
        data.numero_documento,
    )
    if exists:
        obj = repositories.edit_chofer_by_propietario(
            exists,
            db,
            data,
            foto_documento_frente_url,
            foto_documento_reverso_url,
            foto_perfil_url,
            foto_registro_frente_url,
            foto_registro_reverso_url,
            modified_by,
        )
        edit_gestor_carga_chofer(db, obj, gestor_cuenta_id, data.alias, modified_by)
    else:
        delete_chofer_by_id(db, chofer_id, modified_by)
        obj = repositories.create_chofer_by_propietario(
            db,
            data,
            gestor_cuenta_id,
            foto_documento_frente_url,
            foto_documento_reverso_url,
            foto_perfil_url,
            foto_registro_frente_url,
            foto_registro_reverso_url,
            modified_by,
        )
        create_gestor_carga_chofer(db, obj, gestor_cuenta_id, data.alias, modified_by)
    return get_chofer_detail(db, obj, gestor_cuenta_id)


def delete_chofer_by_id(
    db: Session,
    chofer_id: Optional[int],
    modified_by: str,
):
    if chofer_id:
        chofer = repositories.get_chofer_by_id(db, chofer_id)
        if chofer:
            repositories.delete_chofer(chofer, db, modified_by)
