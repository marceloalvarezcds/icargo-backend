from typing import Any, List

from fastapi import APIRouter, Depends, Form, Request
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum
from app.models import User

api = APIRouter()


@api.get("/gestor_carga_id", response_model=List[schemas.User])
async def read_user_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.USER)),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return services.get_user_list_by_gestor_carga_id(db, current_user.gestor_carga_id)


@api.get("/active_list", response_model=List[schemas.User])
async def read_user_active_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.USER)),  # noqa: B008
):
    return services.get_user_active_list_by_gestor_carga_id(
        db, current_user.gestor_carga_id
    )


@api.get("/me", response_model=schemas.UserAccount)
def my_account(
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.USER)),  # noqa: B008
) -> Any:
    """
    Retrieve current user.
    """
    return current_user


@api.get("/{id}", response_model=schemas.User)
async def read_user_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.USER)),  # noqa: B008
):
    return services.get_user_by_id(db, id)


@api.post("/", response_model=schemas.User)
def create_user(
    request: Request,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.UserCreate] = Form(...),  # type: ignore  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.USER)),  # noqa: B008
) -> Any:
    return services.create_user(
        db, data, current_user.gestor_carga_id, current_user.username, request  # type: ignore
    )


@api.put("/{id}", response_model=schemas.User)
async def edit_user(
    request: Request,
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.UserUpdate] = Form(...),  # type: ignore  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.USER)),  # noqa: B008
):
    return services.edit_user(
        db,
        id,
        data,  # type: ignore
        current_user.gestor_carga_id,
        current_user.username,
        request,
    )


@api.get("/{id}/active", response_model=schemas.User)
def active_user_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.USER)),  # noqa: B008
):
    return services.change_user_status(db, id, EstadoEnum.ACTIVO, current_user.username)


@api.get("/{id}/inactive", response_model=schemas.User)
def inactive_user_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.USER)),  # noqa: B008
):
    return services.change_user_status(
        db, id, EstadoEnum.INACTIVO, current_user.username, current_user.id
    )
