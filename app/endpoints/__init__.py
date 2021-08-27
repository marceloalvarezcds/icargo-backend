from fastapi import APIRouter

from app.db import SessionLocal

from app.schemas import user as user_schema

api = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api.get("/")
def home():
    return {"Hello": "FastAPI"}

from .user import get_user
from .product import get_products
from .product_tag import get_products_tags
from .auth import login
from .preference_category import get_preference_category