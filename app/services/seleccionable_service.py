from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.enums.estado import EstadoEnum
from app.repositories import seleccionable_repository as repository
from app.repositories.seleccionable_repository import Model, Schema


def get_by_descripcion(
    ModelType: type, db: Session, descripcion: str
) -> Optional[Model]:
    return repository.get_by_descripcion(ModelType, db, descripcion)


def get_by_id(ModelType: type, db: Session, id: int) -> Model:
    obj: Optional[Model] = repository.get_by_id(ModelType, db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto no encontrado")
    return obj


def get_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_list(ModelType, db)


def get_active_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_active_list(ModelType, db)


def create(
    ModelType: type,
    db: Session,
    data: Schema,
    modified_by: str,
    message_error: str,
) -> Model:
    check_unique(ModelType, db, None, data.descripcion, message_error)
    return repository.create(ModelType, db, data, modified_by)


def edit(
    ModelType: type,
    db: Session,
    id: int,
    data: Schema,
    modified_by: str,
    message_error: str,
) -> Model:
    check_unique(ModelType, db, id, data.descripcion, message_error)
    obj: Model = get_by_id(ModelType, db, id)
    return repository.edit(obj, db, data, modified_by)


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
    descripcion: str,
    message_error: str,
):
    exists: Optional[Model] = get_by_descripcion(ModelType, db, descripcion)  # type: ignore
    if id:
        if exists and exists.id != id:  # type: ignore
            raise HTTPException(
                status_code=409,
                detail=f"{message_error} con descripción {descripcion} ya existe",
            )
    elif exists:
        raise HTTPException(
            status_code=409,
            detail=f"{message_error} con descripción {descripcion} ya existe",
        )
