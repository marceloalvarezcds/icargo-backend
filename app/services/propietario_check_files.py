from typing import List, Optional, Tuple

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import (
    Chofer,
    GestorCargaPropietario,
    Propietario,
    PropietarioContactoGestorCarga,
)

from .pictshare import upload_and_get_image_url


async def check_files(
    foto_documento_frente_file: Optional[UploadFile],
    foto_documento_reverso_file: Optional[UploadFile],
    foto_perfil_file: Optional[UploadFile],
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    foto_documento_frente_url = (
        await upload_and_get_image_url(foto_documento_frente_file)
        if foto_documento_frente_file
        else None
    )
    foto_documento_reverso_url = (
        await upload_and_get_image_url(foto_documento_reverso_file)
        if foto_documento_reverso_file
        else None
    )
    if (
        foto_documento_frente_url
        and foto_documento_reverso_url
        and foto_documento_frente_url == foto_documento_reverso_url
    ):
        raise HTTPException(
            status_code=400,
            detail="El reverso y el frente del documento no pueden ser las mismas imágenes",
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
    # Datos del chofer
    if obj.chofer:
        chofer: Chofer = obj.chofer
        obj_dict["tipo_documento_id"] = chofer.tipo_documento_id
        obj_dict["tipo_documento"] = chofer.tipo_documento
        obj_dict["pais_emisor_documento_id"] = chofer.pais_emisor_documento_id
        obj_dict["pais_emisor_documento"] = chofer.pais_emisor_documento
        obj_dict["numero_documento"] = chofer.numero_documento
        obj_dict["foto_documento_frente_chofer"] = chofer.foto_documento_frente
        obj_dict["foto_documento_reverso_chofer"] = chofer.foto_documento_reverso
        # inicio registro
        ciudad_emisor_registro = chofer.ciudad_emisor_registro
        localidad_emisor_registro = ciudad_emisor_registro.localidad
        pais_emisor_registro = ciudad_emisor_registro.localidad.pais
        obj_dict["pais_emisor_registro_id"] = pais_emisor_registro.id
        obj_dict["pais_emisor_registro"] = pais_emisor_registro
        obj_dict["localidad_emisor_registro_id"] = localidad_emisor_registro.id
        obj_dict["localidad_emisor_registro"] = localidad_emisor_registro
        obj_dict["ciudad_emisor_registro_id"] = chofer.ciudad_emisor_registro_id
        obj_dict["ciudad_emisor_registro"] = chofer.ciudad_emisor_registro
        obj_dict["tipo_registro_id"] = chofer.tipo_registro_id
        obj_dict["tipo_registro"] = chofer.tipo_registro
        obj_dict["numero_registro"] = chofer.numero_registro
        obj_dict["vencimiento_registro"] = chofer.vencimiento_registro
        obj_dict["foto_registro_frente"] = chofer.foto_registro_frente
        obj_dict["foto_registro_reverso"] = chofer.foto_registro_reverso
        # fin registro
    return schemas.Propietario.parse_obj(obj_dict)


def get_propietario_by_ruc(db: Session, ruc: Optional[str]) -> Optional[Propietario]:
    fisica = repositories.get_tipo_persona_by_descripcion(db, "Física")
    if fisica and ruc:
        return repositories.get_propietario_by(db, fisica.id, ruc)
    return None
