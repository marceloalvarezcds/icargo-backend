from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Unidad


def get_unidad_by_descripcion(db: Session, descripcion: str) -> Optional[Unidad]:
    return db.query(Unidad).filter(Unidad.descripcion == descripcion).first()


def get_unidad_list(db: Session) -> List[Unidad]:
    return (
        db.query(Unidad).order_by(Unidad.descripcion).order_by(Unidad.descripcion).all()
    )
