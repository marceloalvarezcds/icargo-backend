from datetime import datetime
from typing import List, Optional, TypeVar

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models.seleccionable_mixin import SeleccionableMixin
from app.schemas.seleccionable_base_model import SeleccionableFormBaseModel

T = TypeVar("T", bound=SeleccionableMixin)


def get_by_descripcion(Model: type, db: Session, descripcion: str) -> Optional[T]:
    return db.query(Model).filter_by(descripcion=descripcion).first()


def get_by_id(Model: type, db: Session, id: int) -> Optional[T]:
    return db.query(Model).get(id)


def get_list(Model: type, db: Session) -> List[T]:
    return (
        db.query(Model)
        .filter(Model.estado != EstadoEnum.ELIMINADO.value)  # type: ignore
        .order_by(Model.id.desc())  # type: ignore
        .all()
    )


def get_active_list(Model: type, db: Session) -> List[T]:
    return (
        db.query(Model)
        .filter_by(estado=EstadoEnum.ACTIVO.value)
        .order_by(Model.id.desc())  # type: ignore
        .all()
    )


def create(
    Model: type,
    db: Session,
    data: SeleccionableFormBaseModel,
    modified_by: str,
) -> T:
    obj: T = Model(
        descripcion=data.descripcion,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit(
    obj: T,
    db: Session,
    data: SeleccionableFormBaseModel,
    modified_by: str,
) -> T:
    obj.descripcion = data.descripcion  # type: ignore
    obj.modified_by = modified_by  # type: ignore
    obj.modified_at = datetime.now()  # type: ignore
    db.commit()
    db.refresh(obj)
    return obj


def change_status(
    obj: T,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> T:
    obj.estado = status.value  # type: ignore
    obj.modified_by = modified_by  # type: ignore
    obj.modified_at = datetime.now()  # type: ignore
    db.commit()
    db.refresh(obj)
    return obj


def delete(
    obj: T,
    db: Session,
    modified_by: str,
) -> T:
    return change_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
