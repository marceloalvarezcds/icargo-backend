from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import Caja
from app.schemas import CajaForm


def get_caja_list(db: Session) -> List[Caja]:
    return (
        db.query(Caja)
        .filter(Caja.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Caja.nombre)
        .all()
    )


def get_caja_list_by_gestor_carga_id(db: Session, gestor_carga_id: int) -> List[Caja]:
    return (
        db.query(Caja)
        .filter(
            and_(
                Caja.gestor_carga_id == gestor_carga_id,
                Caja.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Caja.nombre)
        .all()
    )


def get_caja_by(db: Session, nombre: str, gestor_carga_id: int) -> Optional[Caja]:
    return (
        db.query(Caja)
        .filter(
            and_(
                Caja.nombre == nombre,
                Caja.gestor_carga_id == gestor_carga_id,
            )
        )
        .first()
    )


def get_caja_by_id(db: Session, id: int) -> Optional[Caja]:
    return db.query(Caja).get(id)


def create_caja(
    db: Session,
    data: CajaForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Caja:
    obj = Caja(
        nombre=data.nombre,
        moneda_id=data.moneda_id,
        gestor_carga_id=gestor_carga_id,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_caja(
    obj: Caja,
    db: Session,
    data: CajaForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Caja:
    obj.nombre = data.nombre
    obj.moneda_id = data.moneda_id
    obj.gestor_carga_id = gestor_carga_id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_caja_status(
    obj: Caja,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Caja:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_caja(
    obj: Caja,
    db: Session,
    modified_by: str,
) -> Caja:
    return change_caja_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
