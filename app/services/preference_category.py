from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas import preference_category as schemas
from app.models import preference_category as models
from . import auth

def get_preference_category_by_id(db: Session, preference_category_id: int):
    try:
        return db.query(models.PreferenceCategory).filter(models.PreferenceCategory.id == preference_category_id).first()
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")

def get_preference_category_all(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.PreferenceCategory).filter(models.PreferenceCategory.is_active == True).offset(skip).limit(limit).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")

def create_preference_category(db: Session, preference_category: schemas.PreferenceCategoryCreate):
    try:
        db_preference_category = models.PreferenceCategory(preference_category.name, preference_category.description)
        db.add(db_preference_category)
        db.commit()
        db.refresh(db_preference_category)
        return db_preference_category
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")

def edit_preference_category(db: Session, id: int, preference_category: schemas.PreferenceCategoryCreate):
    try:
        db_preference_category = get_preference_category_by_id(db, id)
        db_preference_category.name = preference_category.name
        db_preference_category.description = preference_category.description
        db.commit()
        db.refresh(db_preference_category)
        return db_preference_category
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")

def remove_preference_category(db: Session, id: int):
    try:
        db_preference_category = get_preference_category_by_id(db, id)
        db_preference_category.is_active = False
        db.commit()
        db.refresh(db_preference_category)
        return db_preference_category
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected Error")