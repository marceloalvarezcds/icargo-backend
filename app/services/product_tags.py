from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Tag, Product
from app.schemas import product_tag as schemas
from app.services import product as ProductService


def get_products_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag).offset(skip).limit(limit).all()


def get_tags_by_id(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()


def create_product_tag(db: Session, tag: schemas.TagCreate):
    db_tag = Tag(name=tag.name, description=tag.description)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def assignment(tag_id: int, product_id: int, db: Session):
    product_db = ProductService.get_product_by_id(db, product_id)
    tag_db = get_tags_by_id(db, tag_id)
    product_db.tags.append(tag_db)
    db.add(product_db)
    db.commit()
    raise HTTPException(status_code=200, detail="Tag assigned correctly")
