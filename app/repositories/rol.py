from typing import List

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import and_  # type: ignore

from app.enums.rol import CodigoRolEnum
from app.models import Rol, UserRol


def get_rol_list(db: Session) -> List[Rol]:
    return db.query(Rol).order_by(Rol.descripcion).all()


def get_rol_list_by_user_id(db: Session, user_id: int) -> List[Rol]:
    return (
        db.query(Rol)
        .join(UserRol.rol)
        .filter(UserRol.user_id == user_id)
        .order_by(Rol.descripcion)
        .all()
    )


def exists_rol_for_user(db: Session, user_id: int, rol: CodigoRolEnum) -> bool:
    return (
        db.query(UserRol)
        .join(UserRol.rol)
        .filter(
            and_(
                UserRol.user_id == user_id,
                Rol.descripcion == rol.value,
            )
        )
        .count()
    ) > 0
