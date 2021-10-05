from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models import CentroOperativo


def get_centro_operativo_list(db: Session) -> List[CentroOperativo]:
    return db.query(CentroOperativo).all()
