from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from pydantic import ValidationError

from app import schemas
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación expirada, por favor vuelva a ingresar",
        )
    user = token_data.user if token_data.user else None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado en el Token",
        )
    return user
