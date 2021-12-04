from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import Remitente
from app.schemas import RemitenteForm


def get_remitente_list(db: Session) -> List[Remitente]:
    return (
        db.query(Remitente)
        .filter(Remitente.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Remitente.nombre)
        .all()
    )


def get_remitente_by(
    db: Session,
    tipo_documento_id: int,
    numero_documento: str,
) -> Optional[Remitente]:
    return (
        db.query(Remitente)
        .filter(
            and_(
                Remitente.numero_documento == numero_documento,
                Remitente.tipo_documento_id == tipo_documento_id,
            )
        )
        .first()
    )


def get_remitente_by_id(db: Session, id: int) -> Optional[Remitente]:
    return db.query(Remitente).filter(Remitente.id == id).first()


def create_remitente(
    db: Session,
    data: RemitenteForm,
    logo_url: str,
    modified_by: str,
) -> Remitente:
    obj = Remitente(
        nombre=data.nombre,
        nombre_corto=data.nombre_corto,
        tipo_documento_id=data.tipo_documento_id,
        numero_documento=data.numero_documento,
        digito_verificador=data.digito_verificador,
        composicion_juridica_id=data.composicion_juridica_id,
        logo=logo_url,
        estado=EstadoEnum.ACTIVO.value,
        telefono=data.telefono,
        email=data.email,
        pagina_web=data.pagina_web,
        info_complementaria=data.info_complementaria,
        direccion=data.direccion,
        latitud=data.latitud,
        longitud=data.longitud,
        ciudad_id=data.ciudad_id,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_remitente(
    obj: Remitente,
    db: Session,
    data: RemitenteForm,
    logo_url: Optional[str],
    modified_by: str,
) -> Remitente:
    obj.nombre = data.nombre
    obj.nombre_corto = data.nombre_corto
    obj.tipo_documento_id = data.tipo_documento_id
    obj.numero_documento = data.numero_documento
    obj.digito_verificador = data.digito_verificador
    obj.composicion_juridica_id = data.composicion_juridica_id
    obj.telefono = data.telefono
    obj.email = data.email
    obj.pagina_web = data.pagina_web
    obj.info_complementaria = data.info_complementaria
    obj.direccion = data.direccion
    obj.latitud = data.latitud
    obj.longitud = data.longitud
    obj.ciudad_id = data.ciudad_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    if logo_url:
        obj.logo = logo_url
    db.commit()
    db.refresh(obj)
    return obj


def delete_remitente(
    obj: Remitente,
    db: Session,
    modified_by: str,
) -> Remitente:
    obj.estado = EstadoEnum.ELIMINADO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
