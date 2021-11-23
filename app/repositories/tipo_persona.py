from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoPersona


def get_tipo_persona_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoPersona]:
    return db.query(TipoPersona).filter(TipoPersona.descripcion == descripcion).first()


def get_tipo_persona_list(db: Session) -> List[TipoPersona]:
    return db.query(TipoPersona).order_by(TipoPersona.descripcion).all()
