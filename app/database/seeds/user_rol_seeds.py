from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Permiso, User, UserRol
from app.services import edit_or_create_rol_by_descripcion
from app.services.generic_service import get_by_unique_columns_or_none


def user_rol_seeds(
    db: Session,
    user: User,
    rol_descripcion: str,
    permisos: List[Permiso],
    gestor_carga_id: Optional[int] = None,
    modified_by: str = "system",
):
    rol = edit_or_create_rol_by_descripcion(
        db, rol_descripcion, permisos, gestor_carga_id, modified_by
    )
    exists: Optional[UserRol] = get_by_unique_columns_or_none(
        UserRol,
        db,
        user_id=user.id,
        rol_id=rol.id,
    )
    if not exists:
        user.user_roles.append(
            UserRol(
                user_id=user.id,
                rol_id=rol.id,
                created_by=modified_by,
                modified_by=modified_by,
            )
        )
        user.modified_by = modified_by
        db.commit()
