from datetime import timedelta
from types import FunctionType
from typing import Optional

from fastapi import HTTPException, Request  # type: ignore
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt  # type: ignore
from pydantic import ValidationError
from sqlalchemy.orm import Session  # type: ignore

from app.audits import AuditAuth
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.constants import AUTHORIZATION
from app.models.user import User
from app.repositories.user import get, get_by_username
from app.schemas import TokenPayload
from app.services.security import create_access_token
from app.utils.security import get_payload_from_token, verify_password


def authenticate(db: Session, *, username: str, password: str) -> Optional[User]:
    user = get_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_user_from_token(db: Session, *, token: str) -> Optional[User]:
    try:
        payload = get_payload_from_token(token)
        token_data = TokenPayload(**payload)
        return get(db, id=token_data.sub)
    except (jwt.JWTError, ValidationError):
        return None


def get_user_from_request(request: Request, database_connection_function: FunctionType):
    auth = request.headers.get(AUTHORIZATION)
    scheme, token = auth.split()
    if scheme.lower() != "basic":
        db_conn = database_connection_function()
        db = Session(bind=db_conn)
        return get_user_from_token(db, token=token)


def register_audit_auth(db: Session, *, user: User, action: str, ip: str):
    db_audit = AuditAuth(
        action=action,
        user_id=user.id,
        user=user.email,
        ip=ip,
    )
    db.add(db_audit)
    db.commit()


def login(db: Session, *, request: Request, form_data: OAuth2PasswordRequestForm):
    user = authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_activated:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    register_audit_auth(db, user=user, action="login", ip=request.client.host)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
