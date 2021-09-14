from fastapi import HTTPException, Request  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models.user import User


def create_user(
    db: Session,
    *,
    user_in: schemas.UserCreate,
    request: Request,
) -> User:
    user = repositories.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = repositories.user.create(db, obj_in=user_in, request=request)
    return user
