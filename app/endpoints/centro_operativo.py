from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import get_db_session, reusable_oauth2

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
