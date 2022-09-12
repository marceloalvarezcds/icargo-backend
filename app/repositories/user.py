from typing import List, Optional

from sqlalchemy import literal, select  # type: ignore
from sqlalchemy.engine.row import Row  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.sqltypes import BigInteger  # type: ignore

from app.models.user import User, UserRol


def get_user_by_id(db: Session, id: BigInteger) -> Optional[User]:
    return db.query(User).get(id)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_id_by_rol_id(db: Session, rol_id: int) -> List[Row]:
    return db.execute(select(UserRol.user_id).where(UserRol.rol_id == rol_id)).all()


def exists_user_for_rol_id(db: Session, rol_id: int) -> bool:
    return (
        db.query(literal(True))
        .filter(db.query(UserRol).filter(UserRol.rol_id == rol_id).exists())
        .scalar()
    )


def get_user_list_by_punto_venta_id(db: Session, punto_venta_id: int) -> List[User]:
    return db.query(User).filter(User.punto_venta_id == punto_venta_id).all()
