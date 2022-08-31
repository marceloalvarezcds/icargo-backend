from typing import List, Optional, Tuple

from fastapi import UploadFile
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import Chofer, GestorCargaChofer
from app.services import propietario_check_files

from .pictshare import check_duplicate_images


async def check_files(
    foto_documento_frente_file: Optional[UploadFile],
    foto_documento_reverso_file: Optional[UploadFile],
    foto_registro_frente_file: Optional[UploadFile],
    foto_registro_reverso_file: Optional[UploadFile],
    foto_perfil_file: Optional[UploadFile] = None,
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    (
        foto_documento_frente_url,
        foto_documento_reverso_url,
        foto_perfil_url,
    ) = await propietario_check_files.check_files(
        foto_documento_frente_file,
        foto_documento_reverso_file,
        foto_perfil_file,
    )
    (
        foto_registro_frente_url,
        foto_registro_reverso_url,
    ) = await check_duplicate_images(
        foto_registro_frente_file,
        foto_registro_reverso_file,
        "El reverso y el frente del registro no pueden ser las mismas imágenes",
    )
    return (
        foto_documento_frente_url,
        foto_documento_reverso_url,
        foto_registro_reverso_url,
        foto_registro_frente_url,
        foto_perfil_url,
    )


def get_chofer_detail(
    db: Session, model: Chofer, gestor_cuenta_id: Optional[int]
) -> schemas.Chofer:
    obj = schemas.Chofer.from_orm(model)
    ges: List[GestorCargaChofer] = model.gestores
    gestores = [x for x in ges if x.gestor_carga_id == gestor_cuenta_id]
    obj.gestor_carga_chofer = gestores[0] if len(gestores) > 0 else None
    obj.oc_with_anticipos_liberados = (
        repositories.get_orden_carga_with_anticipo_liberado_count_by_chofer_id(
            db, obj.id
        )
    )
    # Obteniendo los datos del propietario
    propietario = propietario_check_files.get_propietario_by_ruc(db, model.ruc)
    if propietario:
        obj.pais_origen_id = propietario.pais_origen_id
        obj.pais_origen = propietario.pais_origen
        obj.foto_documento_frente_propietario = propietario.foto_documento_frente
        obj.foto_documento_reverso_propietario = propietario.foto_documento_reverso
    return obj
