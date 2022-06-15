from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.enums.estado import EstadoEnum
from app.repositories import generic_repository as repository
from app.repositories.generic_repository import Model, Schema
from app.utils.gestor_carga import get_gestor_carga_by_params


def get_by_id(ModelType: type, db: Session, id: int) -> Model:
    obj: Optional[Model] = repository.get_by_id(ModelType, db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto no encontrado")
    return obj


def get_by_unique_columns(
    ModelType: type, db: Session, **filter_columns
) -> Optional[Model]:
    return repository.get_by_unique_columns(ModelType, db, **filter_columns)


def get_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_list(ModelType, db)


def get_list_by_gestor_carga_id(
    ModelType: type, db: Session, gestor_carga_id: int
) -> List[Model]:
    return repository.get_list_by_gestor_carga_id(ModelType, db, gestor_carga_id)


def get_active_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_active_list(ModelType, db)


def get_active_list_by_gestor_carga_id(
    ModelType: type, db: Session, gestor_carga_id: int
) -> List[Model]:
    return repository.get_active_list_by_gestor_carga_id(ModelType, db, gestor_carga_id)


def create(
    ModelType: type,
    db: Session,
    data: Schema,
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> Model:
    check_unique(ModelType, db, None, unique_message_error, **unique_columns)
    return repository.create(ModelType, db, data, modified_by)


def create_with_gestor_carga_id(
    ModelType: type,
    db: Session,
    data: Schema,
    gestor_carga_id: int,
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> Model:
    check_unique(ModelType, db, None, unique_message_error, **unique_columns)
    gestor_id = get_gestor_carga_by_params(data, gestor_carga_id)
    return repository.create_with_gestor_carga_id(
        ModelType, db, data, gestor_id, modified_by
    )


def edit(
    ModelType: type,
    db: Session,
    id: int,
    data: Schema,
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> Model:
    check_unique(ModelType, db, id, unique_message_error, **unique_columns)
    obj: Model = get_by_id(ModelType, db, id)
    return repository.edit(obj, db, data, modified_by)


def edit_with_gestor_carga_id(
    ModelType: type,
    db: Session,
    id: int,
    data: Schema,
    gestor_carga_id: int,
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> Model:
    check_unique(ModelType, db, id, unique_message_error, **unique_columns)
    gestor_id = get_gestor_carga_by_params(data, gestor_carga_id)
    obj: Model = get_by_id(ModelType, db, id)
    return repository.edit_with_gestor_carga_id(obj, db, data, gestor_id, modified_by)


def change_status(
    ModelType: type,
    db: Session,
    id: int,
    status: EstadoEnum,
    modified_by: str,
) -> Model:
    obj: Model = get_by_id(ModelType, db, id)
    return repository.change_status(obj, db, status, modified_by)


def delete(
    ModelType: type,
    db: Session,
    id: int,
    modified_by: str,
) -> Model:
    obj: Model = get_by_id(ModelType, db, id)
    return repository.delete(obj, db, modified_by)


def check_unique(
    ModelType: type,
    db: Session,
    id: Optional[int],
    unique_message_error: str,
    **unique_columns,
):
    exists: Optional[Model] = get_by_unique_columns(ModelType, db, **unique_columns)  # type: ignore  # noqa: B950
    if id:
        if exists and exists.id != id:  # type: ignore
            raise HTTPException(
                status_code=409,
                detail=unique_message_error,
            )
    elif exists:
        raise HTTPException(
            status_code=409,
            detail=unique_message_error,
        )
