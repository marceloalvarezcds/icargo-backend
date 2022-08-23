from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Caja])
async def read_caja_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAJA)),  # noqa: B008
):
    return repositories.get_caja_list(db)


@api.get("/gestor_carga_id", response_model=List[schemas.Caja])
async def read_caja_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAJA)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_caja_list(db, current_user.gestor_carga_id)


@api.get("/reports")
async def caja_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.CAJA)),  # noqa: B008
):
    return services.get_caja_reports(db)


@api.get("/{id}", response_model=schemas.Caja)
async def read_caja_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CAJA)),  # noqa: B008
):
    return services.get_caja_by_id(db, id)


@api.post("/", response_model=schemas.Caja)
async def add_new_caja(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CajaForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.CAJA)),  # noqa: B008
):
    return services.create_caja(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Caja)
async def edit_caja(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CajaForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.CAJA)),  # noqa: B008
):
    return services.edit_caja(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Caja)
async def delete_caja(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.CAJA)),  # noqa: B008
):
    return services.delete_caja(db, id, current_user.username)
