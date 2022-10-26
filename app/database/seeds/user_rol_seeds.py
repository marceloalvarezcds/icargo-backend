from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Permiso, Rol, RolPermiso, User, UserRol
from app.repositories import get_permiso_list_by_rol_id
from app.schemas import RolCreate
from app.services import create_rol
from app.services.generic_service import get_by_unique_columns_or_none


def user_rol_seeds(
    db: Session,
    user: User,
    rol_descripcion: str,
    permisos: List[Permiso],
    gestor_carga_id: Optional[int] = None,
    modified_by: str = "system",
):
    rol: Optional[Rol] = get_by_unique_columns_or_none(
        Rol, db, descripcion=rol_descripcion, gestor_carga_id=gestor_carga_id
    )
    if rol:
        permiso_id_list = [x.id for x in get_permiso_list_by_rol_id(db, rol.id)]
        for p in permisos:
            if p.id not in permiso_id_list:
                permiso_id_list.append(p.id)
                rol.roles_permisos.append(
                    RolPermiso(
                        rol_id=rol.id,
                        permiso_id=p.id,
                        created_by=modified_by,
                        modified_by=modified_by,
                    )
                )
        db.commit()
    else:
        permiso_list = []
        permiso_id_list = []
        for p in permisos:
            if p.id not in permiso_id_list:
                permiso_list.append(p)
                permiso_id_list.append(p.id)
        rol = create_rol(
            db,
            RolCreate(
                descripcion=rol_descripcion,
                permisos=permiso_list,
                gestor_carga_id=gestor_carga_id,
            ),
            gestor_carga_id,
            modified_by,
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
