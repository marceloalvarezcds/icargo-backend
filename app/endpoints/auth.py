from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from . import api, get_db
from app.config import TokenSettings
from app.services import auth as auth_services
from app.services import user as user_services
from app.models import user as user_models
from app.schemas import user as schemas

token_settings = TokenSettings()

@api.post(
    "/login/",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {"user": "string", "access_token": "string", "token_type": "bearer"}
                }
            },
        },
    },
    tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    access_token_expires = timedelta(minutes=token_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_services.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"user": user.email, "access_token": access_token, "token_type": "bearer"}

@api.post("/login-external/",
          responses={
              200: {
                  "description": "Successful Response",
                  "content": {
                      "application/json": {
                          "example": {"user": "string", "access_token": "string", "token_type": "bearer"}
                      }
                  },
              },
          },
          tags=["auth"])
def external_login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_services.get_user_by_email(db, email=user.email)
    if (db_user):
        if (db_user.google_user == user.google_user and db_user.fb_user == user.fb_user and db_user.apple_user == user.apple_user):
            return auth_services.set_user_token(db_user)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Email is not registered with selected signup, try again with another login option")
    else:
        new_user = user_services.create_user(db, user)
        return auth_services.set_user_token(user)

