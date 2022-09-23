from http import HTTPStatus

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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = token_data.user if token_data.user else None
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


async def get_current_punto_venta_user(
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
) -> schemas.AuthPuntoVentaUser:
    if not current_user.punto_venta_id:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, "Este usuario no pertenece a un Punto de Venta"
        )
    return schemas.AuthPuntoVentaUser(
        id=current_user.id,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_admin=current_user.is_admin,
        gestor_carga_id=current_user.gestor_carga_id,
        punto_venta_id=current_user.punto_venta_id,
    )


async def get_current_punto_venta_admin_user(
    current_user: schemas.AuthPuntoVentaUser = Depends(  # noqa: B008
        get_current_punto_venta_user
    ),
) -> schemas.AuthPuntoVentaUser:
    if not current_user.is_admin:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, "Este usuario no es administrador del Punto de Venta"
        )
    return current_user


async def get_current_punto_venta_no_admin_user(
    current_user: schemas.AuthPuntoVentaUser = Depends(  # noqa: B008
        get_current_punto_venta_user
    ),
) -> schemas.AuthPuntoVentaUser:
    if current_user.is_admin:
        raise HTTPException(
            HTTPStatus.FORBIDDEN, "Este usuario es Administrador del Punto de Venta"
        )
    return current_user
