from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoSemi


def get_tipo_semi_by_descripcion(db: Session, descripcion: str) -> Optional[TipoSemi]:
    return db.query(TipoSemi).filter(TipoSemi.descripcion == descripcion).first()


def get_tipo_semi_list(db: Session) -> List[TipoSemi]:
    return db.query(TipoSemi).order_by(TipoSemi.descripcion).all()
