from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from pydantic import ValidationError
from sqlalchemy.orm import Session  # type: ignore

from app import models, schemas, services
from app.dependencies.database_session import get_db_session
from app.utils import get_payload_from_token

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(reusable_oauth2),  # noqa: B008
) -> schemas.AuthUser:
    try:
        payload = get_payload_from_token(token)
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = token_data.user if token_data.user else None
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_user_in_db(
    db: Session = Depends(get_db_session),  # noqa: B008
    token: str = Depends(reusable_oauth2),  # noqa: B008
) -> models.User:
    try:
        payload = get_payload_from_token(token)
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = services.get_user_by_id(db, token_data.sub) if token_data.sub else None
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
