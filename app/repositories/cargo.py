from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Cargo


def get_cargo_by_descripcion(db: Session, descripcion: str) -> Optional[Cargo]:
    return db.query(Cargo).filter(Cargo.descripcion == descripcion).first()


def get_cargo_list(db: Session) -> List[Cargo]:
    return db.query(Cargo).order_by(Cargo.descripcion).all()
