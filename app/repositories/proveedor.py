from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import Proveedor, ProveedorContactoGestorCarga
from app.schemas import ProveedorForm


def get_proveedor_list(db: Session) -> List[Proveedor]:
    return (
        db.query(Proveedor)
        .filter(Proveedor.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Proveedor.nombre)
        .all()
    )


def get_proveedor_list_by_gestor_cuenta_id(
    db: Session, gestor_cuenta_id: int
) -> List[Proveedor]:
    return (
        db.query(Proveedor)
        .filter(
            and_(
                Proveedor.estado != EstadoEnum.ELIMINADO.value,
                Proveedor.contactos.any(
                    ProveedorContactoGestorCarga.gestor_carga_id == gestor_cuenta_id
                ),
            )
        )
        .order_by(Proveedor.nombre)
        .all()
    )


def get_proveedor_by(
    db: Session,
    tipo_documento_id: int,
    numero_documento: str,
) -> Optional[Proveedor]:
    return (
        db.query(Proveedor)
        .filter(
            and_(
                Proveedor.numero_documento == numero_documento,
                Proveedor.tipo_documento_id == tipo_documento_id,
            )
        )
        .first()
    )


def get_proveedor_by_id(db: Session, id: int) -> Optional[Proveedor]:
    return db.query(Proveedor).filter(Proveedor.id == id).first()


def create_proveedor(
    db: Session,
    data: ProveedorForm,
    logo_url: Optional[str],
    modified_by: str,
) -> Proveedor:
    obj = Proveedor(
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
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_proveedor(
    obj: Proveedor,
    db: Session,
    data: ProveedorForm,
    logo_url: Optional[str],
    modified_by: str,
) -> Proveedor:
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


def delete_proveedor(
    obj: Proveedor,
    db: Session,
    modified_by: str,
) -> Proveedor:
    obj.estado = EstadoEnum.ELIMINADO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
