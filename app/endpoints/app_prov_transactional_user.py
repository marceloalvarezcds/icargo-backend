from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso
from app.dependencies import get_current_punto_venta_admin_user as get_current_user
from app.dependencies import get_db_session
from app.enums import EstadoEnum
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import TransactionalUser
from app.schemas import ApiResponseData
from app.services import generic_app_response_service as service

api = APIRouter()


@api.get("/", response_model=ApiResponseData[List[schemas.TransactionalUser]])
async def read_transactional_user_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthPuntoVentaUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TRANSACTIONAL_USER)),  # noqa: B008
):
    return service.get_list_by_filter(
        TransactionalUser,
        schemas.TransactionalUser,
        db,
        punto_venta_id=current_user.punto_venta_id,
    )


@api.get("/{id}", response_model=ApiResponseData[schemas.TransactionalUser])
async def read_transactional_user_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.TRANSACTIONAL_USER)),  # noqa: B008
):
    return service.get_by_id(TransactionalUser, schemas.TransactionalUser, db, id)


@api.post("/", response_model=ApiResponseData[schemas.TransactionalUser])
async def add_new_transactional_user(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: schemas.TransactionalUserCreateForm = Body(...),  # noqa: B008
    current_user: schemas.AuthPuntoVentaUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.TRANSACTIONAL_USER)),  # noqa: B008
):
    return services.create_transactional_user_with_pin(
        db,
        data,
        current_user,
    )


@api.put("/{id}", response_model=ApiResponseData[schemas.TransactionalUser])
async def edit_transactional_user(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: schemas.TransactionalUserEditForm = Body(...),  # noqa: B008
    current_user: schemas.AuthPuntoVentaUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.TRANSACTIONAL_USER)),  # noqa: B008
):
    data.punto_venta_id = current_user.punto_venta_id
    return service.edit(
        TransactionalUser,
        schemas.TransactionalUser,
        db,
        id,
        data,  # type: ignore
        current_user.username,
        "El usuario transaccional",
        punto_venta_id=data.punto_venta_id,
        numero_documento=data.numero_documento,
    )


@api.get("/{id}/active", response_model=ApiResponseData[schemas.TransactionalUser])
def active_transactional_user_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthPuntoVentaUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TRANSACTIONAL_USER)),  # noqa: B008
):
    return service.change_status(
        TransactionalUser,
        schemas.TransactionalUser,
        db,
        id,
        EstadoEnum.ACTIVO,
        current_user.username,
    )


@api.get("/{id}/inactive", response_model=ApiResponseData[schemas.TransactionalUser])
def inactive_transactional_user_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthPuntoVentaUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TRANSACTIONAL_USER)),  # noqa: B008
):
    return service.change_status(
        TransactionalUser,
        schemas.TransactionalUser,
        db,
        id,
        EstadoEnum.INACTIVO,
        current_user.username,
    )


@api.get(
    "/{id}/generate_pin", response_model=ApiResponseData[schemas.TransactionalUser]
)
def generate_pin_transactional_user_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthPuntoVentaUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.TRANSACTIONAL_USER)),  # noqa: B008
):
    return services.update_pin_by_id(db, id, current_user.punto_venta_id)
