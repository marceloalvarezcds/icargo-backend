from http.client import BAD_REQUEST
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.cache.permiso import reset_permiso_in_cache_by_user_id
from app.enums.estado import EstadoEnum
from app.models import Rol, RolPermiso
from app.models.user import User
from app.repositories import exists_user_for_rol_id, get_user_id_by_rol_id
from app.schemas import PermisoChecked, RolCreate, RolUpdate
from app.services import generic_service as service


def get_rol_by_id(db: Session, id: int) -> List[Rol]:
    return service.get_by_id(Rol, db, id)


def get_rol_list(db: Session, gestor_carga_id: Optional[int]) -> List[Rol]:
    return service.get_list_all_or_by_gestor_carga_id(Rol, db, gestor_carga_id)


def get_rol_active_list(db: Session, gestor_carga_id: Optional[int]) -> List[Rol]:
    return service.get_active_list_by_gestor_carga_id(Rol, db, gestor_carga_id)


unique_message_error = "Este rol ya existe en el sistema"


def create_rol(
    db: Session,
    data: RolCreate,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Rol:
    permisos: List[PermisoChecked] = data.permisos
    del data.permisos
    if not data.gestor_carga_id and gestor_carga_id:
        data.gestor_carga_id = gestor_carga_id
    rol: Rol = service.create(
        Rol,
        db,
        data,
        modified_by,
        unique_message_error,
        descripcion=data.descripcion,
        gestor_carga_id=data.gestor_carga_id,
    )
    save_permisos(db, rol, permisos, modified_by)
    return rol


def edit_rol(
    db: Session,
    id: int,
    data: RolUpdate,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Rol:
    permisos: List[PermisoChecked] = data.permisos
    del data.permisos
    if not data.gestor_carga_id and gestor_carga_id:
        data.gestor_carga_id = gestor_carga_id
    rol: Rol = service.edit(
        Rol,
        db,
        id,
        data,
        modified_by,
        unique_message_error,
        descripcion=data.descripcion,
        gestor_carga_id=data.gestor_carga_id,
    )
    save_permisos(db, rol, permisos, modified_by)
    return rol


def change_rol_status(
    db: Session,
    id: int,
    status: EstadoEnum,
    modified_by: str,
) -> Rol:
    if status == EstadoEnum.INACTIVO:
        exists_user_for_rol = exists_user_for_rol_id(db, id)
        if exists_user_for_rol:
            m = "No puede Desactivar un rol cuando está relacionado a uno o más usuarios"
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=m,
            )
    return service.change_status(Rol, db, id, status, modified_by)


def delete_rol(
    db: Session,
    id: int,
    modified_by: str,
) -> Rol:
    return service.delete(Rol, db, id, modified_by)


def save_permisos(
    db: Session, rol: Rol, permisos: List[PermisoChecked], modified_by: str
):
    rol.roles_permisos = []
    db.commit()
    for permiso in permisos:
        rol.roles_permisos.append(
            RolPermiso(
                rol_id=rol.id,
                permiso_id=permiso.id,
                created_by=modified_by,
                modified_by=modified_by,
            )
        )
    db.commit()
    # reinicia la cache de permisos de los usuarios del rol para que vuelva a consultar de la base de datos  # noqa: B950
    user_id_tuple_list = get_user_id_by_rol_id(db, rol.id)
    for user_id_tuple in user_id_tuple_list:
        if user_id_tuple:
            user_id: int = user_id_tuple[0]
            reset_permiso_in_cache_by_user_id(user_id)


def get_roles_by_user_id(db: Session, user_id: int) -> List[Rol]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [user_rol.rol for user_rol in user.user_roles]
