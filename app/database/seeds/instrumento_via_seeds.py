from sqlalchemy.orm import Session  # type: ignore

from app.enums import InstrumentoViaEnum
from app.models import InstrumentoVia
from app.repositories import get_instrumento_via_by_descripcion


def create_instrumento_via(db: Session, descripcion: str):
    instrumento_via = get_instrumento_via_by_descripcion(db, descripcion)
    if instrumento_via is None:
        instrumento_via = InstrumentoVia(descripcion=descripcion)
        db.add(instrumento_via)
        db.commit()


def instrumento_via_seeds(db: Session):
    create_instrumento_via(db, InstrumentoViaEnum.CAJA.value)
    create_instrumento_via(db, InstrumentoViaEnum.BANCO.value)
