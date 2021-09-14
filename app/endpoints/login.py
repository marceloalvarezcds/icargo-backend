from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import services
from app.dependencies import get_db_session
from app.schemas.token import Token

api = APIRouter()


@api.post("/", response_model=Token)
def login(
    request: Request,
    db: Session = Depends(get_db_session),  # noqa: B008
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    return services.login(db, request=request, form_data=form_data)
