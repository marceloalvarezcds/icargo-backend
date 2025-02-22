from typing import List, Optional, cast

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


def get_by_unique_columns_or_none(
    ModelType: type, db: Session, should_throw_exception: bool = False, **filter_columns
) -> Optional[Model]:
    obj: Optional[Model] = repository.get_by_unique_columns(
        ModelType, db, **filter_columns
    )
    if not obj and should_throw_exception:
        raise HTTPException(status_code=404, detail="Objeto no encontrado")
    return obj


def get_by_unique_columns(ModelType: type, db: Session, **filter_columns) -> Model:
    return cast(
        Model,
        get_by_unique_columns_or_none(
            ModelType, db, should_throw_exception=True, **filter_columns
        ),
    )


def get_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_list(ModelType, db)


def get_list_by_filter(ModelType: type, db: Session, **filter_columns) -> List[Model]:
    return repository.get_list_by_filter(ModelType, db, **filter_columns)


def get_list_by_gestor_carga_id(
    ModelType: type, db: Session, gestor_carga_id: int
) -> List[Model]:
    return repository.get_list_by_gestor_carga_id(ModelType, db, gestor_carga_id)


def get_list_all_or_by_gestor_carga_id(
    ModelType: type, db: Session, gestor_carga_id: Optional[int]
) -> List[Model]:
    if gestor_carga_id:
        return get_list_by_gestor_carga_id(ModelType, db, gestor_carga_id)
    return get_list(ModelType, db)


def get_active_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_active_list(ModelType, db)


def get_active_list_by_gestor_carga_id(
    ModelType: type, db: Session, gestor_carga_id: Optional[int]
) -> List[Model]:
    if gestor_carga_id:
        return repository.get_active_list_by_gestor_carga_id(
            ModelType, db, gestor_carga_id
        )
    return get_active_list(ModelType, db)


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


def create_oc(
    ModelType: type,
    db: Session,
    data: Schema,
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> Model:
    check_unique_oc(ModelType, db, None, unique_message_error, **unique_columns)
    return repository.create(ModelType, db, data, modified_by)


def create_with_gestor_carga_id(
    ModelType: type,
    db: Session,
    data: Schema,
    gestor_id: Optional[int],
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> Model:
    check_unique(ModelType, db, None, unique_message_error, **unique_columns)
    gestor_id = get_gestor_carga_by_params(data, gestor_id)
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
    gestor_id: Optional[int],
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> Model:
    check_unique(ModelType, db, id, unique_message_error, **unique_columns)
    gestor_id = get_gestor_carga_by_params(data, gestor_id)
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
    exists: Optional[Model] = get_by_unique_columns_or_none(ModelType, db, **unique_columns)  # type: ignore  # noqa: B950
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


def check_unique_oc(
    ModelType: type,
    db: Session,
    id: Optional[int],
    unique_message_error: str,
    skip_unique_check: bool = False,  # Nuevo parámetro para omitir la verificación de unicidad
    **unique_columns,
):
    if skip_unique_check:
        return True  # Si se debe omitir la verificación, simplemente retorna True

    exists: Optional[Model] = get_by_unique_columns_or_none(ModelType, db, **unique_columns)  # type: ignore  # noqa: B950
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
    return True
