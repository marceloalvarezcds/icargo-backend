from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums.estado import EstadoEnum
from app.repositories.generic_repository import Model, Schema
from app.schemas import ApiResponseData

from . import generic_service as service


def _api_response_obj(SchemaType: Schema, obj: Model) -> ApiResponseData[Schema]:
    return ApiResponseData(data=SchemaType.from_orm(obj))


def _api_response_list(
    SchemaType: Schema, lista: List[Model]
) -> ApiResponseData[List[Schema]]:
    return ApiResponseData(data=[SchemaType.from_orm(x) for x in lista])


def get_by_id(
    ModelType: type, SchemaType: Schema, db: Session, id: int
) -> ApiResponseData[Schema]:
    return _api_response_obj(SchemaType, service.get_by_id(ModelType, db, id))


def get_by_unique_columns(
    ModelType: type, SchemaType: Schema, db: Session, **filter_columns
) -> ApiResponseData[Schema]:
    return _api_response_obj(
        SchemaType, service.get_by_unique_columns(ModelType, db, **filter_columns)
    )


def get_list(
    ModelType: type, SchemaType: Schema, db: Session
) -> ApiResponseData[List[Schema]]:
    return _api_response_list(SchemaType, service.get_list(ModelType, db))


def get_list_by_filter(
    ModelType: type, SchemaType: Schema, db: Session, **filter_columns
) -> ApiResponseData[List[Schema]]:
    return _api_response_list(
        SchemaType, service.get_list_by_filter(ModelType, db, **filter_columns)
    )


def get_list_by_gestor_carga_id(
    ModelType: type, SchemaType: Schema, db: Session, gestor_carga_id: int
) -> ApiResponseData[List[Schema]]:
    return _api_response_list(
        SchemaType, service.get_list_by_gestor_carga_id(ModelType, db, gestor_carga_id)
    )


def get_list_all_or_by_gestor_carga_id(
    ModelType: type, SchemaType: Schema, db: Session, gestor_carga_id: Optional[int]
) -> ApiResponseData[List[Schema]]:
    return _api_response_list(
        SchemaType,
        service.get_list_all_or_by_gestor_carga_id(ModelType, db, gestor_carga_id),
    )


def get_active_list(
    ModelType: type, SchemaType: Schema, db: Session
) -> ApiResponseData[List[Schema]]:
    return _api_response_list(SchemaType, service.get_active_list(ModelType, db))


def get_active_list_by_gestor_carga_id(
    ModelType: type, SchemaType: Schema, db: Session, gestor_carga_id: Optional[int]
) -> ApiResponseData[List[Schema]]:
    return _api_response_list(
        SchemaType,
        service.get_active_list_by_gestor_carga_id(ModelType, db, gestor_carga_id),
    )


def create(
    ModelType: type,
    SchemaType: Schema,
    db: Session,
    data: Schema,
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> ApiResponseData[Schema]:
    return _api_response_obj(
        SchemaType,
        service.create(
            ModelType, db, data, modified_by, unique_message_error, **unique_columns
        ),
    )


def create_with_gestor_carga_id(
    ModelType: type,
    SchemaType: Schema,
    db: Session,
    data: Schema,
    gestor_id: Optional[int],
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> ApiResponseData[Schema]:
    return _api_response_obj(
        SchemaType,
        service.create_with_gestor_carga_id(
            ModelType,
            db,
            data,
            gestor_id,
            modified_by,
            unique_message_error,
            **unique_columns,
        ),
    )


def edit(
    ModelType: type,
    SchemaType: Schema,
    db: Session,
    id: int,
    data: Schema,
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> ApiResponseData[Schema]:
    return _api_response_obj(
        SchemaType,
        service.edit(
            ModelType, db, id, data, modified_by, unique_message_error, **unique_columns
        ),
    )


def edit_with_gestor_carga_id(
    ModelType: type,
    SchemaType: Schema,
    db: Session,
    id: int,
    data: Schema,
    gestor_id: Optional[int],
    modified_by: str,
    unique_message_error: str,
    **unique_columns,
) -> ApiResponseData[Schema]:
    return _api_response_obj(
        SchemaType,
        service.edit_with_gestor_carga_id(
            ModelType,
            db,
            id,
            data,
            gestor_id,
            modified_by,
            unique_message_error,
            **unique_columns,
        ),
    )


def change_status(
    ModelType: type,
    SchemaType: Schema,
    db: Session,
    id: int,
    status: EstadoEnum,
    modified_by: str,
) -> ApiResponseData[Schema]:
    return _api_response_obj(
        SchemaType, service.change_status(ModelType, db, id, status, modified_by)
    )


def delete(
    ModelType: type,
    SchemaType: Schema,
    db: Session,
    id: int,
    modified_by: str,
) -> ApiResponseData[Schema]:
    return _api_response_obj(SchemaType, service.delete(ModelType, db, id, modified_by))
