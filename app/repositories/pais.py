from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Pais


def get_pais_by_nombre_corto(db: Session, nombre_corto: str) -> Optional[Pais]:
    return db.query(Pais).filter(Pais.nombre_corto == nombre_corto).first()


def get_pais_list(db: Session) -> List[Pais]:
    return db.query(Pais).all()
