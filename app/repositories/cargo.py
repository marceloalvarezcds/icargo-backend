from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Cargo


def get_cargo_by_descripcion(db: Session, descripcion: str) -> Optional[Cargo]:
    return db.query(Cargo).filter(Cargo.descripcion == descripcion).first()
