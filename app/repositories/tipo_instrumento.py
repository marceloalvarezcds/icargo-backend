from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoInstrumento


def get_tipo_instrumento_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoInstrumento]:
    return (
        db.query(TipoInstrumento)
        .filter(TipoInstrumento.descripcion == descripcion)
        .first()
    )


def get_tipo_instrumento_list(db: Session) -> List[TipoInstrumento]:
    return db.query(TipoInstrumento).order_by(TipoInstrumento.descripcion).all()


def get_tipo_instrumento_list_by_via_id(
    db: Session, via_id: int
) -> List[TipoInstrumento]:
    return (
        db.query(TipoInstrumento)
        .filter(TipoInstrumento.via_id == via_id)
        .order_by(TipoInstrumento.descripcion)
        .all()
    )
