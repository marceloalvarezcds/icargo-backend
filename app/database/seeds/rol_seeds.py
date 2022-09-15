from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import CodigoRolEnum
from app.models import Permiso
from app.services import edit_or_create_rol_by_descripcion

from .permiso_seeds.entities_permiso_seeds import permiso_transactional_user_seeds
from .permiso_seeds.orden_carga_permiso_seeds import (
    permiso_orden_carga_anticipo_retirado_seeds,
    permiso_orden_carga_anticipo_saldo_seeds,
)


def rol_seeds(
    db: Session, gestor_carga_id: Optional[int] = None, modified_by: str = "system"
):
    rol_admin_app_proveedor_seeds(db, gestor_carga_id, modified_by)
    rol_user_app_proveedor_seeds(db, gestor_carga_id, modified_by)


def create_rol(
    db: Session,
    descripcion: str,
    permisos: List[Permiso],
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    edit_or_create_rol_by_descripcion(
        db, descripcion, permisos, gestor_carga_id, modified_by
    )


def rol_admin_app_proveedor_seeds(
    db: Session, gestor_carga_id: Optional[int], modified_by: str
):
    permisos = []
    permisos.extend(permiso_transactional_user_seeds(db))
    create_rol(
        db,
        CodigoRolEnum.ADMIN_APP_PROVEEDOR.value,
        permisos,
        gestor_carga_id,
        modified_by,
    )


def rol_user_app_proveedor_seeds(
    db: Session, gestor_carga_id: Optional[int], modified_by: str
):
    permisos = []
    permisos.extend(permiso_orden_carga_anticipo_retirado_seeds(db))
    permisos.extend(permiso_orden_carga_anticipo_saldo_seeds(db))
    create_rol(
        db,
        CodigoRolEnum.USUARIO_APP_PROVEEDOR.value,
        permisos,
        gestor_carga_id,
        modified_by,
    )
