from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import and_  # type: ignore

from app.models import Ciudad


def get_ciudad_by_nombre_and_localidad_id(
    db: Session, nombre: str, localidad_id: int
) -> Optional[Ciudad]:
    return (
        db.query(Ciudad)
        .filter(and_(Ciudad.nombre == nombre, Ciudad.localidad_id == localidad_id))
        .first()
    )


def get_ciudad_list_by_localidad_id(db: Session, localidad_id: int) -> List[Ciudad]:
    return (
        db.query(Ciudad)
        .filter(Ciudad.localidad_id == localidad_id)
        .order_by(Ciudad.nombre)
        .all()
    )


def get_ciudad_list(db: Session) -> List[Ciudad]:
    return db.query(Ciudad).order_by(Ciudad.nombre).all()
