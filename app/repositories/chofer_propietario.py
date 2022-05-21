from datetime import datetime
from typing import Optional, cast

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Chofer, Propietario, TipoPersona
from app.schemas import ChoferForm

from .tipo_persona import get_tipo_persona_by_descripcion


def create_propietario_by_chofer(
    db: Session,
    data: ChoferForm,
    gestor_cuenta_id: Optional[int],
    foto_documento_frente_url: Optional[str],
    foto_documento_reverso_url: Optional[str],
    foto_perfil_url: Optional[str],
    chofer: Chofer,
    modified_by: str,
) -> Propietario:
    fisica = get_tipo_persona_by_descripcion(db, "Física")
    obj = Propietario(
        nombre=data.nombre,
        tipo_persona_id=cast(TipoPersona, fisica).id,
        ruc=data.ruc,
        digito_verificador=data.digito_verificador,
        pais_origen_id=data.pais_origen_id,
        fecha_nacimiento=data.fecha_nacimiento,
        gestor_cuenta_id=gestor_cuenta_id,
        oficial_cuenta_id=data.oficial_cuenta_id,
        es_chofer=True,
        foto_documento_frente=foto_documento_frente_url,
        foto_documento_reverso=foto_documento_reverso_url,
        foto_perfil=foto_perfil_url,
        estado=EstadoEnum.PENDIENTE.value,
        telefono=data.telefono,
        email=data.email,
        direccion=data.direccion,
        ciudad_id=data.ciudad_id,
        chofer_id=chofer.id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_propietario_by_chofer(
    obj: Propietario,
    db: Session,
    data: ChoferForm,
    foto_documento_frente_url: Optional[str],
    foto_documento_reverso_url: Optional[str],
    foto_perfil_url: Optional[str],
    chofer: Chofer,
    modified_by: str,
) -> Propietario:
    fisica = get_tipo_persona_by_descripcion(db, "Física")
    obj.ruc = data.ruc
    obj.tipo_persona_id = cast(TipoPersona, fisica).id
    obj.digito_verificador = data.digito_verificador
    obj.fecha_nacimiento = data.fecha_nacimiento
    obj.es_chofer = True
    obj.email = data.email
    obj.direccion = data.direccion
    obj.ciudad_id = data.ciudad_id
    obj.chofer_id = chofer.id
    if data.nombre:
        obj.nombre = data.nombre
    if data.pais_origen_id:
        obj.pais_origen_id = data.pais_origen_id
    if data.oficial_cuenta_id:
        obj.oficial_cuenta_id = data.oficial_cuenta_id
    if data.telefono:
        obj.telefono = data.telefono
    if foto_documento_frente_url:
        obj.foto_documento_frente = foto_documento_frente_url
    if foto_documento_reverso_url:
        obj.foto_documento_reverso = foto_documento_reverso_url
    if foto_perfil_url:
        obj.foto_perfil = foto_perfil_url
    obj.estado = EstadoEnum.PENDIENTE.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
