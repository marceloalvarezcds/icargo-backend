from typing import List

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import get_current_user, get_db_session, reusable_oauth2

api = APIRouter()


@api.get("/", response_model=List[schemas.CentroOperativoList])
async def read_centro_operativo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return repositories.get_centro_operativo_list(db)


@api.get("/reports")
async def centro_operativo_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return services.get_centro_operativo_reports(db)


@api.post("/", response_model=schemas.CentroOperativo)
async def add_new_centro_operativo(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CentroOperativoForm] = Form(...),  # type: ignore  # noqa: B008
    file: UploadFile = File(...),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return await services.create_centro_operativo(
        db, data, file, modified_by=current_user.username
    )
