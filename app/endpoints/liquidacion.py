from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Liquidacion])
async def read_liquidacion_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.LIQUIDACION)),  # noqa: B008
):
    return repositories.get_liquidacion_list(db)


@api.get("/gestor_carga_id", response_model=List[schemas.Liquidacion])
async def read_liquidacion_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.LIQUIDACION)),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return services.get_liquidacion_list(db, current_user.gestor_carga_id)


@api.get("/reports")
async def liquidacion_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.LIQUIDACION)),  # noqa: B008
):
    return services.get_liquidacion_reports(db)


@api.get("/{id}", response_model=schemas.Liquidacion)
async def read_liquidacion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.LIQUIDACION)),  # noqa: B008
):
    return services.get_liquidacion_by_id(db, id)


@api.post("/", response_model=schemas.Liquidacion)
async def add_new_liquidacion(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.LiquidacionForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.create_liquidacion(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Liquidacion)
async def edit_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.LiquidacionForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.edit_liquidacion(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Liquidacion)
async def delete_liquidacion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.LIQUIDACION)),  # noqa: B008
):
    return services.delete_liquidacion(db, id, current_user.username)
