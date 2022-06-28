from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models import Rol


def get_rol_list(db: Session) -> List[Rol]:
    return db.query(Rol).order_by(Rol.descripcion).all()
