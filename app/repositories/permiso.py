from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import and_  # type: ignore

from app.enums import PermisoAccionEnum, PermisoModeloEnum
from app.models import Permiso, RolPermiso, UserRol


def exists_permiso_for_user(
    db: Session,
    user_id: int,
    accion: PermisoAccionEnum,
    modelo: PermisoModeloEnum,
) -> int:
    return (
        db.query(UserRol, RolPermiso, Permiso)
        .select_from(UserRol)
        .join(RolPermiso, UserRol.rol_id == RolPermiso.rol_id)
        .join(Permiso, RolPermiso.permiso_id == Permiso.id)
        .filter(
            and_(
                UserRol.user_id == user_id,
                Permiso.accion == accion.value,
                Permiso.modelo == modelo.value,
            )
        )
        .count()
    )


def get_permiso_by(
    db: Session,
    accion: PermisoAccionEnum,
    modelo: PermisoModeloEnum,
) -> Optional[Permiso]:
    return (
        db.query(Permiso)
        .filter(
            and_(
                Permiso.accion == accion.value,
                Permiso.modelo == modelo.value,
            )
        )
        .first()
    )


def get_permiso_list(db: Session) -> List[Permiso]:
    return (
        db.query(Permiso)
        .order_by(Permiso.modulo, Permiso.modelo_titulo, Permiso.modelo, Permiso.accion)
        .all()
    )


def get_permiso_list_by_rol_id(db: Session, rol_id: int) -> List[Permiso]:
    return (
        db.query(Permiso)
        .join(RolPermiso.permiso)
        .filter(RolPermiso.rol_id == rol_id)
        .order_by(Permiso.id)
        .all()
    )


def get_permiso_list_by_user_id(db: Session, user_id: int) -> List[Permiso]:
    return (
        db.query(Permiso)
        .join(RolPermiso, RolPermiso.permiso_id == Permiso.id)
        .join(UserRol, RolPermiso.rol_id == UserRol.rol_id)
        .filter(UserRol.user_id == user_id)
        .order_by(Permiso.id)
        .all()
    )
