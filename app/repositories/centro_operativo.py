from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import CentroOperativo
from app.schemas.centro_operativo import CentroOperativoForm


def get_centro_operativo_list(db: Session) -> List[CentroOperativo]:
    return (
        db.query(CentroOperativo)
        .filter(CentroOperativo.estado != EstadoEnum.ELIMINADO.value)
        .all()
    )


def get_centro_operativo_by(
    db: Session, nombre: str, clasificacion_id: int, ciudad_id: int
) -> Optional[CentroOperativo]:
    return (
        db.query(CentroOperativo)
        .filter(
            and_(
                CentroOperativo.nombre == nombre,
                CentroOperativo.clasificacion_id == clasificacion_id,
                CentroOperativo.ciudad_id == ciudad_id,
            )
        )
        .first()
    )


def get_centro_operativo_by_id(db: Session, id: int) -> Optional[CentroOperativo]:
    return db.query(CentroOperativo).filter(CentroOperativo.id == id).first()


def create_centro_operativo(
    db: Session,
    data: CentroOperativoForm,
    logo_url: str,
    modified_by: str,
) -> CentroOperativo:
    obj = CentroOperativo(
        nombre=data.nombre,
        nombre_corto=data.nombre_corto,
        logo=logo_url,
        estado=EstadoEnum.ACTIVO.value,
        telefono=data.telefono,
        email=data.email,
        pagina_web=data.pagina_web,
        direccion=data.direccion,
        latitud=data.latitud,
        longitud=data.longitud,
        clasificacion_id=data.clasificacion_id,
        ciudad_id=data.ciudad_id,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_centro_operativo(
    obj: CentroOperativo,
    db: Session,
    data: CentroOperativoForm,
    logo_url: Optional[str],
    modified_by: str,
) -> CentroOperativo:
    obj.nombre = data.nombre
    obj.nombre_corto = data.nombre_corto
    obj.telefono = (data.telefono,)
    obj.email = (data.email,)
    obj.pagina_web = (data.pagina_web,)
    obj.direccion = data.direccion
    obj.latitud = data.latitud
    obj.longitud = data.longitud
    obj.clasificacion_id = data.clasificacion_id
    obj.ciudad_id = data.ciudad_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    if logo_url:
        obj.logo = logo_url
    db.commit()
    db.refresh(obj)
    return obj


def delete_centro_operativo(
    obj: CentroOperativo,
    db: Session,
    modified_by: str,
) -> CentroOperativo:
    obj.estado = EstadoEnum.ELIMINADO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
