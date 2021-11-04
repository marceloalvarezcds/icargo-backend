from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import and_  # type: ignore

from app.models import Localidad


def get_localidad_by_nombre_and_pais_id(
    db: Session, nombre: str, pais_id: int
) -> Optional[Localidad]:
    return (
        db.query(Localidad)
        .filter(and_(Localidad.nombre == nombre, Localidad.pais_id == pais_id))
        .first()
    )


def get_localidad_list(db: Session, pais_id: int) -> List[Localidad]:
    return (
        db.query(Localidad)
        .filter(Localidad.pais_id == pais_id)
        .order_by(Localidad.nombre)
        .all()
    )
