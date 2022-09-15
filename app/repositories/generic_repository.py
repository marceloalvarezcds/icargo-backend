from datetime import datetime
from typing import List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.enums import EstadoEnum

Model = TypeVar("Model", bound=AuditMixin)
Schema = TypeVar("Schema", bound=BaseModel)


def get_by_id(ModelType: type, db: Session, id: int) -> Optional[Model]:
    return db.query(ModelType).get(id)


def get_by_unique_columns(
    ModelType: type, db: Session, **filter_columns
) -> Optional[Model]:
    return db.query(ModelType).filter_by(**filter_columns).first()


def get_list(ModelType: type, db: Session) -> List[Model]:
    return (
        db.query(ModelType)
        .filter(ModelType.estado != EstadoEnum.ELIMINADO.value)  # type: ignore
        .order_by(ModelType.id.desc())  # type: ignore
        .all()
    )


def get_list_by_filter(ModelType: type, db: Session, **filter_columns) -> List[Model]:
    return db.query(ModelType).filter_by(**filter_columns).all()


def get_list_by_gestor_carga_id(
    ModelType: type, db: Session, gestor_carga_id: int
) -> List[Model]:
    return (
        db.query(ModelType)
        .filter((ModelType.estado != EstadoEnum.ELIMINADO.value) & (ModelType.gestor_carga_id == gestor_carga_id))  # type: ignore  # noqa: B950
        .order_by(ModelType.id.desc())  # type: ignore
        .all()
    )


def get_active_list(ModelType: type, db: Session) -> List[Model]:
    return (
        db.query(ModelType)
        .filter(ModelType.estado == EstadoEnum.ACTIVO.value)  # type: ignore
        .order_by(ModelType.id.desc())  # type: ignore
        .all()
    )


def get_active_list_by_gestor_carga_id(
    ModelType: type, db: Session, gestor_carga_id: int
) -> List[Model]:
    return (
        db.query(ModelType)
        .filter((ModelType.estado == EstadoEnum.ACTIVO.value) & (ModelType.gestor_carga_id == gestor_carga_id))  # type: ignore  # noqa: B950
        .order_by(ModelType.id.desc())  # type: ignore
        .all()
    )


def create(
    ModelType: type,
    db: Session,
    data: Schema,
    modified_by: str,
) -> Model:
    obj: Model = ModelType(
        **data.dict(),
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_with_gestor_carga_id(
    ModelType: type,
    db: Session,
    data: Schema,
    gestor_carga_id: int,
    modified_by: str,
) -> Model:
    data.gestor_carga_id = gestor_carga_id  # type: ignore
    return create(ModelType, db, data, modified_by)


def edit(
    obj: Model,
    db: Session,
    data: Schema,
    modified_by: str,
) -> Model:
    for prop, value in data.dict().items():
        if hasattr(obj, prop) and value:
            setattr(obj, prop, value)
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def edit_with_gestor_carga_id(
    obj: Model,
    db: Session,
    data: Schema,
    gestor_carga_id: int,
    modified_by: str,
) -> Model:
    data.gestor_carga_id = gestor_carga_id  # type: ignore
    return edit(obj, db, data, modified_by)


def change_status(
    obj: Model,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Model:
    obj.estado = status.value  # type: ignore
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete(
    obj: Model,
    db: Session,
    modified_by: str,
) -> Model:
    return change_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
