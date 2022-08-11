from typing import List, Optional, Tuple

from fastapi import UploadFile
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import (
    GestorCargaPropietario,
    Propietario,
    PropietarioContactoGestorCarga,
)

from .pictshare import check_duplicate_images, upload_and_get_image_url


async def check_files(
    foto_documento_frente_file: Optional[UploadFile],
    foto_documento_reverso_file: Optional[UploadFile],
    foto_perfil_file: Optional[UploadFile],
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    (
        foto_documento_frente_url,
        foto_documento_reverso_url,
    ) = await check_duplicate_images(
        foto_documento_frente_file,
        foto_documento_reverso_file,
        "El reverso y el frente del documento no pueden ser las mismas imágenes",
    )
    foto_perfil_url = (
        await upload_and_get_image_url(foto_perfil_file) if foto_perfil_file else None
    )
    return (
        foto_documento_frente_url,
        foto_documento_reverso_url,
        foto_perfil_url,
    )


def get_propietario_detail(
    db: Session, model: Propietario, gestor_cuenta_id: Optional[int]
) -> schemas.Propietario:
    obj = schemas.Propietario.from_orm(model)
    contactos: List[PropietarioContactoGestorCarga] = model.contactos
    ges: List[GestorCargaPropietario] = model.gestores
    gestores = [x for x in ges if x.gestor_carga_id == gestor_cuenta_id]
    obj.contactos = [x for x in contactos if x.gestor_carga_id == gestor_cuenta_id]
    obj.gestor_carga_propietario = gestores[0] if len(gestores) > 0 else None
    obj.oc_with_anticipos_liberados = (
        repositories.get_orden_carga_with_anticipo_liberado_count_by_propietario_id(
            db, obj.id
        )
    )
    return obj


def get_propietario_by_ruc(db: Session, ruc: Optional[str]) -> Optional[Propietario]:
    fisica = repositories.get_tipo_persona_by_descripcion(db, "Física")
    if fisica and ruc:
        return repositories.get_propietario_by(db, fisica.id, ruc)
    return None
