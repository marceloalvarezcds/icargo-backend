from datetime import datetime
from http.client import BAD_REQUEST
from typing import List, Optional

from fastapi import HTTPException, Request  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums.estado import EstadoEnum
from app.models import User, UserRol
from app.repositories import user
from app.schemas import RolChecked, UserCreate, UserUpdate
from app.services import generic_service as service
from app.utils.security import get_md5_hash_hexdigest, get_password_hash


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return user.get_user_by_email(db, email)


def get_user_by_id(db: Session, id: int) -> User:
    obj = user.get_user_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obj


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return user.get_user_by_username(db, username)


def get_user_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[User]:
    return service.get_list_all_or_by_gestor_carga_id(User, db, gestor_carga_id)


def get_user_active_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: int
) -> List[User]:
    return service.get_active_list_by_gestor_carga_id(User, db, gestor_carga_id)


unique_message_error = "Este nombre de usuario ya existe en el sistema"


def create_user(
    db: Session,
    data: UserCreate,
    gestor_carga_id: Optional[int],
    modified_by: str,
    request: Request,
) -> User:
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


def edit_user(
    db: Session,
    id: int,
    data: UserUpdate,
    gestor_carga_id: Optional[int],
    modified_by: str,
    request: Request,
) -> User:
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


def change_user_status(
    db: Session,
    id: int,
    status: EstadoEnum,
    modified_by: str,
    current_user_id: Optional[int] = None,
) -> User:
    if status == EstadoEnum.INACTIVO and current_user_id == id:
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail="No puede Desactivar su propio usuario",
        )
    return service.change_status(User, db, id, status, modified_by)


def delete_user(
    db: Session,
    id: int,
    modified_by: str,
) -> User:
    return service.delete(User, db, id, modified_by)


def set_extra_data_in_create(obj_in: UserCreate, request: Request) -> UserCreate:
    created_at = datetime.now()
    string_to_hash = "%s-%s-%s" % (created_at, obj_in.email, obj_in.username)
    ip = request.client.host
    # Settea valores extras
    obj_in.token = get_md5_hash_hexdigest(string_to_hash)
    obj_in.password = get_password_hash(obj_in.password)
    obj_in.surname = obj_in.username
    obj_in.created_ip_address = ip
    obj_in.last_ip_address = ip
    del obj_in.confirm_password
    return obj_in


def set_extra_data_in_edit(obj_in: UserUpdate, request: Request) -> UserUpdate:
    ip = request.client.host
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
    db.commit()
