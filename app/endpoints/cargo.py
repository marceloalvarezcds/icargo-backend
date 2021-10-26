from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.dependencies import get_db_session, reusable_oauth2

api = APIRouter()


@api.get("/", response_model=List[schemas.Cargo])
async def read_cargo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: str = Depends(reusable_oauth2),  # noqa: B008
):
    return repositories.get_cargo_list(db)
