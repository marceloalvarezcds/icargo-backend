from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Rol


def get_rol_by_codigo(db: Session, codigo: str) -> Optional[Rol]:
    return db.query(Rol).filter(Rol.codigo == codigo).first()


def get_rol_list(db: Session) -> List[Rol]:
    return db.query(Rol).all()
