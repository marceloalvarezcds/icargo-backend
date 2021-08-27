from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas import user as schemas
from app.models import user as models
from . import auth


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed_password, name=user.name, last_name=user.last_name,
                            phone_number=user.phone_number, ruc=user.ruc, icargo_user=user.icargo_user, google_user=user.google_user,
                            fb_user=user.fb_user, apple_user=user.apple_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def edit_user(db: Session, user_id: int, user: schemas.UserCreate):
    try:
        db_user = get_user_by_id(db, user_id)
        db_user.email = user.email
        db_user.name = user.name
        db_user.last_name = user.last_name
        db_user.phone_number = user.phone_number
        db_user.ruc = user.ruc
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")


def remove_user(db: Session, user_id: int):
    try:
        db_user = get_user_by_id(db, user_id)
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")
