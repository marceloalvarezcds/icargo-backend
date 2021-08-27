
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.utils import oauth
from app.schemas import user as schemas
from app.models import user as models
from app.services import user as user_services
from app.config import TokenSettings

token_settings = TokenSettings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = oauth.OAuth2PasswordBearerCookie(tokenUrl="login")


def authenticate_user(db, username: str, password: str):
    user = user_services.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def set_user_token(user):
    access_token_expires = timedelta(
        minutes=token_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"user": user.email, "access_token": access_token, "token_type": "bearer"}


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, token_settings.SECRET_KEY, algorithm=token_settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, token_settings.SECRET_KEY,
                             algorithms=[token_settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data_user = username
    except JWTError:
        raise credentials_exception

    return token_data_user
