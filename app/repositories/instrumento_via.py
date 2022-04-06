from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import InstrumentoVia


def get_instrumento_via_by_descripcion(
    db: Session, descripcion: str
) -> Optional[InstrumentoVia]:
    return (
        db.query(InstrumentoVia)
        .filter(InstrumentoVia.descripcion == descripcion)
        .first()
    )


def get_instrumento_via_by_id(db: Session, id: int) -> Optional[InstrumentoVia]:
    return db.query(InstrumentoVia).get(id)


def get_instrumento_via_list(db: Session) -> List[InstrumentoVia]:
    return db.query(InstrumentoVia).order_by(InstrumentoVia.descripcion).all()
