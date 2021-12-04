from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Color


def get_color_by_descripcion(db: Session, descripcion: str) -> Optional[Color]:
    return db.query(Color).filter(Color.descripcion == descripcion).first()


def get_color_list(db: Session) -> List[Color]:
    return db.query(Color).order_by(Color.descripcion).order_by(Color.descripcion).all()
