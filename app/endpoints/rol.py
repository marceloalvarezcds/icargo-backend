from typing import Any, List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum
from app.models import User

api = APIRouter()


@api.get("/", response_model=List[schemas.Rol])
async def read_rol_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ROL)),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return services.get_rol_list(db, current_user.gestor_carga_id)


@api.get("/active_list", response_model=List[schemas.Rol])
async def read_rol_active_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ROL)),  # noqa: B008
):
    return services.get_rol_active_list(db, current_user.gestor_carga_id)


@api.get("/{id}", response_model=schemas.Rol)
async def read_rol_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ROL)),  # noqa: B008
):
    return services.get_rol_by_id(db, id)


@api.post("/", response_model=schemas.Rol)
def create_rol(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.RolCreate] = Form(...),  # type: ignore  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.ROL)),  # noqa: B008
) -> Any:
    return services.create_rol(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Rol)
async def edit_rol(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.RolUpdate] = Form(...),  # type: ignore  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.ROL)),  # noqa: B008
):
    return services.edit_rol(
        db,
        id,
        data,  # type: ignore
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.get("/{id}/active", response_model=schemas.Rol)
def active_rol_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ROL)),  # noqa: B008
):
    return services.change_rol_status(db, id, EstadoEnum.ACTIVO, current_user.username)


@api.get("/{id}/inactive", response_model=schemas.Rol)
def inactive_rol_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.ROL)),  # noqa: B008
):
    return services.change_rol_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )


@api.delete("/{id}", response_model=schemas.Rol)
async def delete_rol(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.ROL)),  # noqa: B008
):
    return services.delete_rol(db, id, current_user.username)
