from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models import Ciudad


def get_ciudad_list(db: Session, localidad_id: int) -> List[Ciudad]:
    return db.query(Ciudad).filter(Ciudad.localidad_id == localidad_id).all()
