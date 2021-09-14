from typing import Any

from fastapi import APIRouter, Depends, Request  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import models, schemas, services
from app.dependencies import get_current_user, get_db_session

api = APIRouter()


@api.get("/", response_model=schemas.User)
def my_account(
    current_user: models.User = Depends(get_current_user),  # noqa: B008
) -> Any:
    """
    Retrieve current user.
    """
    return current_user


@api.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(get_db_session),  # noqa: B008
    user_in: schemas.UserCreate,
    request: Request,
) -> Any:
    """
    Create new user.
    """
    return services.create_user(db, user_in=user_in, request=request)
