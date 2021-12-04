from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import MarcaSemi


def get_marca_semi_by_descripcion(db: Session, descripcion: str) -> Optional[MarcaSemi]:
    return db.query(MarcaSemi).filter(MarcaSemi.descripcion == descripcion).first()


def get_marca_semi_list(db: Session) -> List[MarcaSemi]:
    return db.query(MarcaSemi).order_by(MarcaSemi.descripcion).all()
