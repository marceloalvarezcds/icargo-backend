from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums.estado import EstadoEnum
from app.models import Rol, RolPermiso
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
