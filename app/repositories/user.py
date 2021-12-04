import datetime
from typing import List, Optional

from fastapi import Request  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.sqltypes import BigInteger  # type: ignore

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_md5_hash_hexdigest, get_password_hash


def create(db: Session, modified_by: str, obj_in: UserCreate, request: Request) -> User:
    created_at = datetime.datetime.now()
    string_to_hash = "%s-%s-%s" % (created_at, obj_in.email, obj_in.username)
    token = get_md5_hash_hexdigest(string_to_hash)
    password = obj_in.password if obj_in.password else ""
    ip = request.client.host
    db_obj = User(
        token=token,
        email=obj_in.email,
        surname=obj_in.surname,
        username=obj_in.username,
        password=get_password_hash(password),
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        is_activated=obj_in.is_activated,
        is_guest=obj_in.is_guest,
        is_superuser=obj_in.is_superuser,
        created_ip_address=ip,
        last_ip_address=ip,
        modified_by=modified_by,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get(db: Session, id: BigInteger) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()


def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_list_by_gestor_carga_id(db: Session, gestor_carga_id: int) -> List[User]:
    return (
        db.query(User)
        .filter(User.gestor_carga_id == gestor_carga_id)
        .order_by(User.first_name.desc(), User.last_name)
        .all()
    )
