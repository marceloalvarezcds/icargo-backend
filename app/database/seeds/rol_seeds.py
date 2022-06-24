from sqlalchemy.orm import Session  # type: ignore

from app.enums import CodigoRolEnum
from app.models import Rol
from app.services.generic_service import get_by_unique_columns


def create_rol(db: Session, codigo: str, descripcion: str):
    rol = get_by_unique_columns(Rol, db, descripcion=descripcion)
    if rol is None:
        rol = Rol(codigo=codigo, descripcion=descripcion)
        db.add(rol)
        db.commit()


def rol_seeds(db: Session):
    create_rol(
        db,
        codigo=CodigoRolEnum.ADMIN_GESTOR_CARGA.value,
        descripcion="Administrador de Gestor de Carga",
    )
    create_rol(
        db,
        codigo=CodigoRolEnum.ADMIN_ICARGO.value,
        descripcion="Administrador de Icargo",
    )
