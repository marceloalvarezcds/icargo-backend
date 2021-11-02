from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import get_current_user, get_db_session, reusable_oauth2

api = APIRouter()


@api.get("/", response_model=List[schemas.RemitenteList])
async def read_remitente_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return repositories.get_remitente_list(db)


@api.get("/reports")
async def remitente_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return services.get_remitente_reports(db)


@api.get("/{id}", response_model=schemas.Remitente)
async def read_remitente_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return services.get_remitente_by_id_and_gestor_carga_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.Remitente)
async def add_new_remitente(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.RemitenteForm] = Form(...),  # type: ignore  # noqa: B008
    file: UploadFile = File(...),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return await services.create_remitente(
        db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Remitente)
async def edit_remitente(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.RemitenteForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return await services.edit_remitente(
        id, db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Remitente)
async def delete_remitente(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return services.delete_remitente(
        db, id, current_user.gestor_carga_id, current_user.username
    )
