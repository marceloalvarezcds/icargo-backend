from typing import List

from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import CentroOperativo
from app.schemas.centro_operativo import CentroOperativoForm


def get_centro_operativo_list(db: Session) -> List[CentroOperativo]:
    return db.query(CentroOperativo).all()


def create_centro_operativo(
    db: Session,
    data: Json[CentroOperativoForm],  # type: ignore
    logo_url: str,
    modified_by: str,
) -> CentroOperativo:
    db_data = CentroOperativo(
        nombre=data.nombre,  # type: ignore
        nombre_corto=data.nombre_corto,  # type: ignore
        logo=logo_url,
        estado=EstadoEnum.ACTIVO.value,
        direccion=data.direccion,  # type: ignore
        latitud=-25.658948139894708,
        longitud=-54.717514329980474,
        clasificacion_id=data.clasificacion_id,  # type: ignore
        ciudad_id=data.ciudad_id,  # type: ignore
        modified_by=modified_by,
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
