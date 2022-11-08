from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import EstadoEnum
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import TipoCuenta
from app.services import seleccionable_service as service

api = APIRouter()


@api.get("/", response_model=List[schemas.TipoCuenta])
async def read_tipo_cuenta_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_CUENTA)),  # noqa: B008
):
    return services.get_tipo_cuenta_list_by_tipo_documento_relacionado_otro(db)


@api.get("/active_list", response_model=List[schemas.TipoCuenta])
async def read_tipo_cuenta_active_list_by_tipo_documento_relacionado_otro(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_CUENTA)),  # noqa: B008
):
    return services.get_tipo_cuenta_active_list_by_tipo_documento_relacionado_otro(db)


@api.get("/{id}", response_model=schemas.TipoCuenta)
async def read_tipo_cuenta_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.TIPO_CUENTA)),  # noqa: B008
):
    return service.get_by_id(TipoCuenta, db, id)


@api.post("/", response_model=schemas.TipoCuenta)
async def add_new_tipo_cuenta(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.TipoCuentaForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.TIPO_CUENTA)),  # noqa: B008
):
    return services.create_tipo_cuenta(db, data, current_user.username)  # type: ignore


@api.put("/{id}", response_model=schemas.TipoCuenta)
async def edit_tipo_cuenta(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.TipoCuentaForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.TIPO_CUENTA)),  # noqa: B008
):
    return service.edit(TipoCuenta, db, id, data, current_user.username, "El Tipo de Cuenta")  # type: ignore  # noqa: B950


@api.get("/{id}/active", response_model=schemas.TipoCuenta)
def active_tipo_cuenta_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TIPO_CUENTA)),  # noqa: B008
):
    return service.change_status(
        TipoCuenta, db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.TipoCuenta)
def inactive_tipo_cuenta_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TIPO_CUENTA)),  # noqa: B008
):
    return service.change_status(
        TipoCuenta, db, id, EstadoEnum.INACTIVO, current_user.username
    )
