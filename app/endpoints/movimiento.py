from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Movimiento])
async def read_movimiento_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
):
    return repositories.get_movimiento_list(db)


@api.get("/gestor_carga_id", response_model=List[schemas.Movimiento])
async def read_movimiento_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return services.get_movimiento_list(db, current_user.gestor_carga_id)


@api.get("/orden_carga/{orden_carga_id}", response_model=List[schemas.Movimiento])
async def read_movimiento_list_by_orden_carga_id(
    orden_carga_id: int,  # noqa: B008
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MOVIMIENTO)),  # noqa: B008
):
    return repositories.get_movimiento_list_by_orden_carga_id(db, orden_carga_id)


@api.get("/reports")
async def movimiento_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.MOVIMIENTO)),  # noqa: B008
):
    return services.get_movimiento_reports(db)


@api.get("/{id}", response_model=schemas.Movimiento)
async def read_movimiento_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.MOVIMIENTO)),  # noqa: B008
):
    return services.get_movimiento_by_id(db, id)


@api.post("/", response_model=schemas.Movimiento)
async def add_new_movimiento(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.create_movimiento(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Movimiento)
async def edit_movimiento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MovimientoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.edit_movimiento(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Movimiento)
async def delete_movimiento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.MOVIMIENTO)),  # noqa: B008
):
    return services.delete_movimiento(db, id, current_user.username)
