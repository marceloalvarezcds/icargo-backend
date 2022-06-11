from typing import Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.sqltypes import BigInteger  # type: ignore

from app.models.user import User


def get_user_by_id(db: Session, id: BigInteger) -> Optional[User]:
    return db.query(User).get(id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()
