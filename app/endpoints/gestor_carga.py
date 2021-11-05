from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import get_current_user, get_db_session, reusable_oauth2

api = APIRouter()


@api.get("/", response_model=List[schemas.GestorCargaList])
async def read_gestor_carga_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return repositories.get_gestor_carga_list(db)


@api.get("/reports")
async def gestor_carga_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return services.get_gestor_carga_reports(db)


@api.get("/{id}", response_model=schemas.GestorCarga)
async def read_gestor_carga_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return services.get_gestor_carga_by_id(db, id)


@api.post("/", response_model=schemas.GestorCarga)
async def add_new_gestor_carga(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.GestorCargaForm] = Form(...),  # type: ignore  # noqa: B008
    file: UploadFile = File(...),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return await services.create_gestor_carga(
        db, data, file, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.GestorCarga)
async def edit_gestor_carga(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.GestorCargaForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return await services.edit_gestor_carga(
        id, db, data, file, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.GestorCarga)
async def delete_gestor_carga(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return services.delete_gestor_carga(db, id, current_user.username)
