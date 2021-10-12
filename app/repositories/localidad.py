from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models import Localidad


def get_localidad_list(db: Session, pais_id: int) -> List[Localidad]:
    return db.query(Localidad).filter(Localidad.pais_id == pais_id).all()
