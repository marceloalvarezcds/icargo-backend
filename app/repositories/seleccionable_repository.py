from typing import List, Optional, TypeVar

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models.seleccionable_mixin import SeleccionableMixin
from app.repositories import generic_repository as repository
from app.schemas.seleccionable_base_model import SeleccionableFormBaseModel

Model = TypeVar("Model", bound=SeleccionableMixin)
Schema = TypeVar("Schema", bound=SeleccionableFormBaseModel)


def get_by_descripcion(
    ModelType: type, db: Session, descripcion: str
) -> Optional[Model]:
    return repository.get_by_unique_columns(ModelType, db, descripcion=descripcion)


def get_by_id(ModelType: type, db: Session, id: int) -> Optional[Model]:
    return repository.get_by_id(ModelType, db, id)


def get_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_list(ModelType, db)


def get_active_list(ModelType: type, db: Session) -> List[Model]:
    return repository.get_active_list(ModelType, db)


def create(
    ModelType: type,
    db: Session,
    data: Schema,
    modified_by: str,
) -> Model:
    return repository.create(ModelType, db, data, modified_by)


def edit(
    obj: Model,
    db: Session,
    data: Schema,
    modified_by: str,
) -> Model:
    return repository.edit(obj, db, data, modified_by)


def change_status(
    obj: Model,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Model:
    return repository.change_status(obj, db, status, modified_by)


def delete(
    obj: Model,
    db: Session,
    modified_by: str,
) -> Model:
    return change_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
