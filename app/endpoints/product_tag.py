from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import product_tag as schemas
from app.services import product_tags as services
from . import api, get_db


@api.get("/tag/products", response_model=List[schemas.Tag], tags=["product_tag"])
def get_products_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products_tags = services.get_products_tags(db, skip=skip, limit=limit)
    return products_tags


@api.post("/tag/products", response_model=schemas.Tag, tags=["product_tag"])
def create_products_tags(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = services.get_tag_by_name(db, name=tag.name)
    if db_tag:
        raise HTTPException(status_code=400, detail="Tag already registered")
    return services.create_product_tag(db=db, tag=tag)


@api.post("/tag/{tag_id}/product/{product_id}", status_code=status.HTTP_200_OK, tags=["product_tag"])
def assignment_tag_product(tag_id: int, product_id: int, db: Session = Depends(get_db)):
    return services.assignment(tag_id=tag_id, product_id=product_id, db=db)
