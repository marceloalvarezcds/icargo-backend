from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, Request  # type: ignore
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt  # type: ignore
from pydantic import ValidationError
from sqlalchemy.orm import Session  # type: ignore
from starlette.datastructures import Headers

from app.audits import AuditAuth
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.constants import AUTHORIZATION
from app.enums.estado import EstadoEnum
from app.models.user import User
from app.schemas import AuthUser, Token, TokenPayload
from app.services.security import create_access_token
from app.utils.security import get_payload_from_token, verify_password

from .user import get_user_by_username


def authenticate(db: Session, *, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Usuario o Contraseña incorrecta")
    elif user.estado == EstadoEnum.INACTIVO.value:
        raise HTTPException(status_code=400, detail="Usuario Inactivo")
    return user


def get_auth_user_from_token(token: str) -> Optional[AuthUser]:
    try:
        payload = get_payload_from_token(token)
        token_data = TokenPayload(**payload)
        return token_data.user
    except (jwt.JWTError, ValidationError):
        return None


def get_authorization_header(headers: Headers) -> str:
    if AUTHORIZATION in headers:
        headers.get(AUTHORIZATION)
    return ""


def get_auth_user_from_authorization_header(auth_header: str) -> Optional[AuthUser]:
    if auth_header:
        scheme, token = auth_header.split()
        if scheme.lower() != "basic":
            return get_auth_user_from_token(token)
    return None


def register_audit_auth(db: Session, *, user: User, action: str, ip: str):
    db_audit = AuditAuth(
        action=action,
        user_id=user.id,
        user=user.email,
        ip=ip,
    )
    db.add(db_audit)
    db.commit()


def create_token_by_user(db: Session, user: User, request: Request) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    register_audit_auth(db, user=user, action="login", ip=request.client.host)
    return Token.parse_obj(
        {
            "access_token": create_access_token(
                AuthUser.from_orm(user), expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    )


def login(
    db: Session, *, request: Request, form_data: OAuth2PasswordRequestForm
) -> Token:
    user = authenticate(db, username=form_data.username, password=form_data.password)
    return create_token_by_user(db, user, request)
