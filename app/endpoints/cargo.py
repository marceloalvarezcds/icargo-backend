from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import EstadoEnum
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import Cargo
from app.schemas.seleccionable_base_model import (
    SeleccionableBaseModel,
    SeleccionableFormBaseModel,
)
from app.services import seleccionable_service as service

api = APIRouter()


@api.get("/", response_model=List[SeleccionableBaseModel])
async def read_cargo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CARGO)),  # noqa: B008
):
    return service.get_list(Cargo, db)


@api.get("/active_list", response_model=List[SeleccionableBaseModel])
async def read_cargo_active_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CARGO)),  # noqa: B008
):
    return service.get_active_list(Cargo, db)


@api.get("/{id}", response_model=SeleccionableBaseModel)
async def read_cargo_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CARGO)),  # noqa: B008
):
    return service.get_by_id(Cargo, db, id)


@api.post("/", response_model=SeleccionableBaseModel)
async def add_new_cargo(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[SeleccionableFormBaseModel] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.CARGO)),  # noqa: B008
):
    return service.create(Cargo, db, data, current_user.username, "El Cargo")  # type: ignore


@api.put("/{id}", response_model=SeleccionableBaseModel)
async def edit_cargo(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[SeleccionableFormBaseModel] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.CARGO)),  # noqa: B008
):
    return service.edit(Cargo, db, id, data, current_user.username, "El Cargo")  # type: ignore


@api.get("/{id}/active", response_model=SeleccionableBaseModel)
def active_cargo_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CARGO)),  # noqa: B008
):
    return service.change_status(
        Cargo, db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=SeleccionableBaseModel)
def inactive_cargo_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CARGO)),  # noqa: B008
):
    return service.change_status(
        Cargo, db, id, EstadoEnum.INACTIVO, current_user.username
    )
