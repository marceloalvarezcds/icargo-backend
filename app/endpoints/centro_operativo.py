from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.CentroOperativoList])
async def read_centro_operativo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return repositories.get_centro_operativo_list(db)


@api.get("/reports")
async def centro_operativo_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.get_centro_operativo_reports(db)


@api.get("/{id}", response_model=schemas.CentroOperativo)
async def read_centro_operativo_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.get_centro_operativo_by_id_and_gestor_carga_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.CentroOperativo)
async def add_new_centro_operativo(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CentroOperativoForm] = Form(...),  # type: ignore  # noqa: B008
    file: UploadFile = File(...),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return await services.create_centro_operativo(
        db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.CentroOperativo)
async def edit_centro_operativo(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CentroOperativoForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return await services.edit_centro_operativo(
        id, db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.CentroOperativo)
async def delete_centro_operativo(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.delete_centro_operativo(
        db, id, current_user.gestor_carga_id, current_user.username
    )
