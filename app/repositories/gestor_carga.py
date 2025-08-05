from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import GestorCarga
from app.schemas import GestorCargaForm


def get_gestor_carga_list(db: Session) -> List[GestorCarga]:
    return (
        db.query(GestorCarga)
        .filter(GestorCarga.estado != EstadoEnum.ELIMINADO.value)
        .order_by(GestorCarga.id.desc())
        .all()
    )


def get_gestor_carga_by(
    db: Session,
    tipo_documento_id: int,
    numero_documento: str,
) -> Optional[GestorCarga]:
    return (
        db.query(GestorCarga)
        .filter(
            and_(
                GestorCarga.numero_documento == numero_documento,
                GestorCarga.tipo_documento_id == tipo_documento_id,
            )
        )
        .first()
    )


def get_gestor_carga_by_id(db: Session, id: int) -> Optional[GestorCarga]:
    return db.query(GestorCarga).filter(GestorCarga.id == id).first()


def create_gestor_carga(
    db: Session,
    data: GestorCargaForm,
    logo_url: Optional[str],
    modified_by: str,
) -> GestorCarga:
    obj = GestorCarga(
        nombre=data.nombre,
        nombre_corto=data.nombre_corto,
        tipo_documento_id=data.tipo_documento_id,
        numero_documento=data.numero_documento,
        digito_verificador=data.digito_verificador,
        composicion_juridica_id=data.composicion_juridica_id,
        moneda_id=data.moneda_id,
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
        limite_cantidad_oc_activas=data.limite_cantidad_oc_activas,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_gestor_carga(
    obj: GestorCarga,
    db: Session,
    data: GestorCargaForm,
    logo_url: Optional[str],
    modified_by: str,
) -> GestorCarga:
    obj.nombre = data.nombre
    obj.nombre_corto = data.nombre_corto
    obj.tipo_documento_id = data.tipo_documento_id
    obj.numero_documento = data.numero_documento
    obj.digito_verificador = data.digito_verificador
    obj.composicion_juridica_id = data.composicion_juridica_id
    obj.moneda_id = data.moneda_id
    obj.telefono = data.telefono
    obj.email = data.email
    obj.pagina_web = data.pagina_web
    obj.info_complementaria = data.info_complementaria
    obj.direccion = data.direccion
    obj.latitud = data.latitud
    obj.longitud = data.longitud
    obj.ciudad_id = data.ciudad_id
    obj.limite_cantidad_oc_activas = data.limite_cantidad_oc_activas
    obj.estado = data.estado
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    if logo_url:
        obj.logo = logo_url
    db.commit()
    db.refresh(obj)
    return obj


def delete_gestor_carga(
    obj: GestorCarga,
    db: Session,
    modified_by: str,
) -> GestorCarga:
    obj.estado = EstadoEnum.ELIMINADO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_gestor_carga_status(
    obj: GestorCarga,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> GestorCarga:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
