from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.enums.estado import EstadoEnum
from app.repositories import seleccionable_repository as repository
from app.repositories.seleccionable_repository import T
from app.schemas.seleccionable_base_model import SeleccionableFormBaseModel


def get_by_descripcion(Model: type, db: Session, descripcion: str) -> Optional[T]:
    return repository.get_by_descripcion(Model, db, descripcion)


def get_by_id(Model: type, db: Session, id: int) -> T:
    obj: Optional[T] = repository.get_by_id(Model, db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto no encontrado")
    return obj


def get_list(Model: type, db: Session) -> List[T]:
    return repository.get_list(Model, db)


def get_active_list(Model: type, db: Session) -> List[T]:
    return repository.get_active_list(Model, db)


def create(
    Model: type,
    db: Session,
    data: SeleccionableFormBaseModel,
    modified_by: str,
    message_error: str,
) -> T:
    if repository.get_by_descripcion(Model, db, data.descripcion):
        raise HTTPException(
            status_code=409,
            detail=f"{message_error} con descripción {data.descripcion} ya existe",
        )
    return repository.create(Model, db, data, modified_by)


def edit(
    Model: type,
    db: Session,
    id: int,
    data: SeleccionableFormBaseModel,
    modified_by: str,
    message_error: str,
) -> T:
    exists: Optional[T] = repository.get_by_descripcion(Model, db, data.descripcion)
    if exists and exists.id != id:
        raise HTTPException(
            status_code=409,
            detail=f"{message_error} con descripción {data.descripcion} ya existe",
        )
    obj: T = get_by_id(Model, db, id)
    return repository.edit(obj, db, data, modified_by)


def change_status(
    Model: type,
    db: Session,
    id: int,
    status: EstadoEnum,
    modified_by: str,
) -> T:
    obj: T = get_by_id(Model, db, id)
    return repository.change_status(obj, db, status, modified_by)


def delete(
    Model: type,
    db: Session,
    id: int,
    modified_by: str,
) -> T:
    obj: T = get_by_id(Model, db, id)
    return repository.delete(obj, db, modified_by)
