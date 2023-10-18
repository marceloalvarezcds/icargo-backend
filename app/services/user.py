from datetime import datetime
from http.client import BAD_REQUEST
from typing import List, Optional

from fastapi import HTTPException, Request  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import schemas
from app.cache.permiso import reset_permiso_in_cache_by_user_id
from app.enums.estado import EstadoEnum
from app.enums.rol import CodigoRolEnum
from app.models import User, UserRol
from app.repositories import (
    exists_rol_for_user,
    get_permiso_list_by_user_id,
    get_rol_list_by_user_id,
    user,
)
from app.schemas import Permiso, RolChecked, UserAccount, UserCreate, UserUpdate
from app.services import generic_service as service
from app.utils import get_host_from_request, get_md5_hash_hexdigest, get_password_hash


def _user_with_rol_list(db: Session, user: User) -> schemas.User:
    schema_user = schemas.User.from_orm(user)
    schema_user.roles = [
        RolChecked.from_orm(r) for r in get_rol_list_by_user_id(db, user.id)
    ]
    return schema_user


def _user_list_with_rol_list(db: Session, user_list: List[User]) -> List[schemas.User]:
    return [_user_with_rol_list(db, u) for u in user_list]


def get_user_account(db: Session, id: int) -> UserAccount:
    user_account = UserAccount.from_orm(get_user_by_id(db, id))
    user_account.permisos = [
        Permiso.from_orm(x) for x in get_permiso_list_by_user_id(db, id)
    ]
    user_account.is_admin_icargo = exists_rol_for_user(
        db, id, CodigoRolEnum.ADMIN_ICARGO
    )
    return user_account


def get_user_by_id(db: Session, id: int) -> User:
    obj = user.get_user_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obj


def get_user_with_rol_list_by_id(db: Session, id: int) -> schemas.User:
    return _user_with_rol_list(db, get_user_by_id(db, id))


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return user.get_user_by_username(db, username)


def get_user_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[User]:
    return service.get_list_all_or_by_gestor_carga_id(User, db, gestor_carga_id)


def get_user_list_with_rol_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[schemas.User]:
    return _user_list_with_rol_list(
        db, get_user_list_by_gestor_carga_id(db, gestor_carga_id)
    )


def get_user_active_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[User]:
    if gestor_carga_id:
        return service.get_active_list_by_gestor_carga_id(User, db, gestor_carga_id)
    return []


unique_message_error = "Este nombre de usuario ya existe en el sistema"


def create_user(
    db: Session,
    data: UserCreate,
    gestor_carga_id: Optional[int],
    modified_by: str,
    request: Request,
) -> User:
    service.check_unique(
        User, db, None, f"Ya existe Usuario con email {data.email}", email=data.email
    )
    roles: List[RolChecked] = data.roles
    del data.roles
    if not data.gestor_carga_id and gestor_carga_id:
        data.gestor_carga_id = gestor_carga_id
    user: User = service.create(
        User,
        db,
        set_extra_data_in_create(data, request),
        modified_by,
        unique_message_error,
        username=data.username,
    )
    save_roles(db, user, roles, modified_by)
    return user


def create_user_with_rol_list(
    db: Session,
    data: UserCreate,
    gestor_carga_id: Optional[int],
    modified_by: str,
    request: Request,
) -> schemas.User:
    user_created = create_user(db, data, gestor_carga_id, modified_by, request)
    return _user_with_rol_list(db, user_created)


def edit_user(
    db: Session,
    id: int,
    data: UserUpdate,
    gestor_carga_id: Optional[int],
    modified_by: str,
    request: Request,
) -> User:
    service.check_unique(
        User, db, id, f"Ya existe Usuario con email {data.email}", email=data.email
    )
    roles: List[RolChecked] = data.roles
    del data.roles
    if not data.gestor_carga_id and gestor_carga_id:
        data.gestor_carga_id = gestor_carga_id
    user: User = service.edit(
        User,
        db,
        id,
        set_extra_data_in_edit(data, request),
        modified_by,
        unique_message_error,
        username=data.username,
    )
    save_roles(db, user, roles, modified_by)
    return user


def edit_user_with_rol_list(
    db: Session,
    id: int,
    data: UserUpdate,
    gestor_carga_id: Optional[int],
    modified_by: str,
    request: Request,
) -> schemas.User:
    user_updated = edit_user(db, id, data, gestor_carga_id, modified_by, request)
    return _user_with_rol_list(db, user_updated)


def change_user_status(
    db: Session,
    id: int,
    status: EstadoEnum,
    modified_by: str,
    current_user_id: Optional[int] = None,
) -> schemas.User:
    if status == EstadoEnum.INACTIVO and current_user_id == id:
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail="No puede Desactivar su propio usuario",
        )
    user: User = service.change_status(User, db, id, status, modified_by)
    return _user_with_rol_list(db, user)


def delete_user(
    db: Session,
    id: int,
    modified_by: str,
) -> schemas.User:
    return _user_with_rol_list(db, service.delete(User, db, id, modified_by))


def set_extra_data_in_create(obj_in: UserCreate, request: Request) -> UserCreate:
    created_at = datetime.now()
    string_to_hash = "%s-%s-%s" % (created_at, obj_in.email, obj_in.username)
    ip = get_host_from_request(request)
    # Settea valores extras
    obj_in.token = get_md5_hash_hexdigest(string_to_hash)
    obj_in.password = get_password_hash(obj_in.password)
    obj_in.surname = obj_in.username
    obj_in.created_ip_address = ip
    obj_in.last_ip_address = ip
    del obj_in.confirm_password
    return obj_in


def set_extra_data_in_edit(obj_in: UserUpdate, request: Request) -> UserUpdate:
    ip = get_host_from_request(request)
    # Settea valores extras
    if obj_in.password:
        obj_in.password = get_password_hash(obj_in.password)
        del obj_in.confirm_password
    obj_in.surname = obj_in.username
    obj_in.last_ip_address = ip
    return obj_in


def save_roles(db: Session, user: User, roles: List[RolChecked], modified_by: str):
    user.user_roles = []
    db.commit()
    for rol in roles:
        user.user_roles.append(
            UserRol(
                rol_id=rol.id,
                user_id=user.id,
                created_by=modified_by,
                modified_by=modified_by,
            )
        )
    # reinicia la cache de permisos del usuario para que vuelva a consultar de la base de datos
    reset_permiso_in_cache_by_user_id(user.id)
    db.commit()
