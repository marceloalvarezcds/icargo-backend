from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Banco])
async def read_banco_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.BANCO)),  # noqa: B008
):
    return repositories.get_banco_list(db)


@api.get("/gestor_carga_id", response_model=List[schemas.Banco])
async def read_banco_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.BANCO)),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return services.get_banco_list(db, current_user.gestor_carga_id)


@api.get("/reports")
async def banco_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.BANCO)),  # noqa: B008
):
    return services.get_banco_reports(db)


@api.get("/{id}", response_model=schemas.Banco)
async def read_banco_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.BANCO)),  # noqa: B008
):
    return services.get_banco_by_id(db, id)


@api.post("/", response_model=schemas.Banco)
async def add_new_banco(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.BancoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.BANCO)),  # noqa: B008
):
    return services.create_banco(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Banco)
async def edit_banco(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.BancoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.BANCO)),  # noqa: B008
):
    return services.edit_banco(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Banco)
async def delete_banco(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.BANCO)),  # noqa: B008
):
    return services.delete_banco(db, id, current_user.username)
