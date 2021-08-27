
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as schemas
from app.services import user as services
from app.services import auth
from . import api, get_db


@api.get("/users/", response_model=List[schemas.User], tags=["user"])
def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip=skip, limit=limit)
    return users


@api.post("/users/", response_model=schemas.User, tags=["user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db=db, user=user)

@api.get("/users/{user_id}/", response_model=schemas.User, tags=["user"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return services.get_user_by_id(db, user_id)

@api.get("/users/me/", tags=["user"])
async def read_users_me(current_user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        user = services.get_user_by_email(db, current_user)
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")
    return user

@api.put("/users/{user_id}/", response_model=schemas.User, tags=["user"])
def edit_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.edit_user(db, user_id, user)

@api.delete("/users/{user_id}", response_model=schemas.User, tags=["user"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return services.remove_user(db, user_id)
