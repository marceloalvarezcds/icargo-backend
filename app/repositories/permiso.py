from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import and_  # type: ignore

from app.enums import PermisoAccionEnum, PermisoModeloEnum
from app.models import Permiso


def get_permiso_by(
    db: Session,
    accion: PermisoAccionEnum,
    modelo: PermisoModeloEnum,
) -> Optional[Permiso]:
    return (
        db.query(Permiso)
        .filter(
            and_(
                Permiso.accion == accion.value,
                Permiso.modelo == modelo.value,
            )
        )
        .first()
    )


def get_permiso_list(db: Session) -> List[Permiso]:
    return (
        db.query(Permiso).order_by(Permiso.modulo, Permiso.modelo, Permiso.accion).all()
    )
