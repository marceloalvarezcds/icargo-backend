from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import CodigoRolEnum
from app.models import Rol


def rol_seeds(db: Session):
    try:
        db.add(
            Rol(
                codigo=CodigoRolEnum.ADMIN_GESTOR_CARGA.value,
                descripcion="Administrador de Gestor de Carga",
            )
        )
        db.add(
            Rol(
                codigo=CodigoRolEnum.ADMIN_ICARGO.value,
                descripcion="Administrador de Icargo",
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
