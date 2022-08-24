from sqlalchemy.orm import Session  # type: ignore

from app.enums import PermisoAccionEnum, PermisoModeloEnum, PermisoModuloEnum
from app.repositories import exists_permiso_for_user


def check_permiso(
    db: Session,
    user_id: int,
    modelo: PermisoModeloEnum,
    accion: PermisoAccionEnum,
    _: PermisoModuloEnum,
) -> bool:
    return exists_permiso_for_user(db, user_id, accion, modelo) > 0
