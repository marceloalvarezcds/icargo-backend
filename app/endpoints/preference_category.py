from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import preference_category as schemas
from app.services import preference_category as services
from . import api, get_db


@api.get("/preference-category/", tags=["preference_category"])
def get_preference_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_preference_category_all(db, skip=skip, limit=limit)


@api.get("/preference-category/{pc_id}", tags=["preference_category"])
def get_preference_category_by_id(pc_id: int, db: Session = Depends(get_db)):
    return services.get_preference_category_by_id(db, pc_id)


@api.post("/preference-category/", tags=["preference_category"])
def create_preference_category(preference_category: schemas.PreferenceCategoryCreate, db: Session = Depends(get_db)):
    return services.create_preference_category(db, preference_category)


@api.put("/preference-category/{pc_id}", tags=["preference_category"])
def edit_preference_category(pc_id: int, preference_category: schemas.PreferenceCategoryCreate, db: Session = Depends(get_db)):
    return services.edit_preference_category(db, pc_id, preference_category)


@api.delete("/preference-category/{pc_id}", tags=["preference_category"])
def delete_preference_category(pc_id: int, db: Session = Depends(get_db)):
    return services.remove_preference_category(db, pc_id)
