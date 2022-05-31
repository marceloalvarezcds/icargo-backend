from typing import List, Optional, Tuple

from fastapi import UploadFile
from sqlalchemy.orm import Session  # type: ignore

from app import schemas
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
    db: Session, obj: Chofer, gestor_cuenta_id: Optional[int]
) -> schemas.Chofer:
    obj_dict = obj.as_dict(for_json=False)
    ges: List[GestorCargaChofer] = obj.gestores
    gestores = [x for x in ges if x.gestor_carga_id == gestor_cuenta_id]
    obj_dict["gestor_carga_chofer"] = gestores[0] if len(gestores) > 0 else None
    obj_dict["tipo_documento"] = obj.tipo_documento
    obj_dict["gestor_cuenta_nombre"] = (
        obj.gestor_cuenta.nombre if obj.gestor_cuenta else None
    )
    obj_dict["oficial_cuenta_nombre"] = obj.oficial_cuenta_nombre
    obj_dict["pais_emisor_documento"] = obj.pais_emisor_documento
    obj_dict["ciudad"] = obj.ciudad
    ciudad_emisor_registro = obj.ciudad_emisor_registro
    localidad_emisor_registro = (
        ciudad_emisor_registro.localidad if ciudad_emisor_registro else None
    )
    pais_emisor_registro = (
        localidad_emisor_registro.pais if localidad_emisor_registro else None
    )
    obj_dict["pais_emisor_registro_id"] = (
        pais_emisor_registro.id if pais_emisor_registro else None
    )
    obj_dict["pais_emisor_registro"] = pais_emisor_registro
    obj_dict["localidad_emisor_registro_id"] = (
        localidad_emisor_registro.id if localidad_emisor_registro else None
    )
    obj_dict["localidad_emisor_registro"] = localidad_emisor_registro
    obj_dict["ciudad_emisor_registro"] = ciudad_emisor_registro
    # Obteniendo los datos del propietario
    propietario = propietario_check_files.get_propietario_by_ruc(db, obj.ruc)
    if propietario:
        obj_dict["pais_origen_id"] = propietario.pais_origen_id
        obj_dict["pais_origen"] = propietario.pais_origen
        obj_dict[
            "foto_documento_frente_propietario"
        ] = propietario.foto_documento_frente
        obj_dict[
            "foto_documento_reverso_propietario"
        ] = propietario.foto_documento_reverso
    return schemas.Chofer.parse_obj(obj_dict)
