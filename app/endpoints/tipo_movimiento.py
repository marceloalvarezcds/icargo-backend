from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import EstadoEnum
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import TipoMovimiento
from app.services import seleccionable_service as service

api = APIRouter()


@api.get("/", response_model=List[schemas.TipoMovimiento])
async def read_tipo_movimiento_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_MOVIMIENTO)),  # noqa: B008
):
    return services.get_tipo_movimiento_list_by_tipo_cuenta_other_than_viajes(db)


@api.get("/cuenta/{cuenta_id}", response_model=List[schemas.TipoMovimiento])
async def read_tipo_movimiento_list_by_cuenta_id(
    cuenta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_MOVIMIENTO)),  # noqa: B008
):
    return services.get_tipo_movimiento_active_list_by_tipo_cuenta_other_than_viajes_and_cuenta_id(  # noqa: B950
        db, cuenta_id
    )


@api.get("/{id}", response_model=schemas.TipoMovimiento)
async def read_tipo_movimiento_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.TIPO_MOVIMIENTO)),  # noqa: B008
):
    return service.get_by_id(TipoMovimiento, db, id)


@api.post("/", response_model=schemas.TipoMovimiento)
async def add_new_tipo_movimiento(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.TipoMovimientoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.TIPO_MOVIMIENTO)),  # noqa: B008
):
    return service.create(TipoMovimiento, db, data, current_user.username, "El Tipo de Movimiento")  # type: ignore  # noqa: B950


@api.put("/{id}", response_model=schemas.TipoMovimiento)
async def edit_tipo_movimiento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.TipoMovimientoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.TIPO_MOVIMIENTO)),  # noqa: B008
):
    return service.edit(TipoMovimiento, db, id, data, current_user.username, "El Tipo de Movimiento")  # type: ignore  # noqa: B950


@api.get("/{id}/active", response_model=schemas.TipoMovimiento)
def active_tipo_movimiento_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TIPO_MOVIMIENTO)),  # noqa: B008
):
    return service.change_status(
        TipoMovimiento, db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.TipoMovimiento)
def inactive_tipo_movimiento_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TIPO_MOVIMIENTO)),  # noqa: B008
):
    return service.change_status(
        TipoMovimiento, db, id, EstadoEnum.INACTIVO, current_user.username
    )
