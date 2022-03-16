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
