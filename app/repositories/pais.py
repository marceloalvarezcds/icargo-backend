from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models import Pais


def get_pais_list(db: Session) -> List[Pais]:
    return db.query(Pais).all()
