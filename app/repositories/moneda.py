from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Moneda


def get_moneda_by_simbolo(db: Session, simbolo: str) -> Optional[Moneda]:
    return db.query(Moneda).filter(Moneda.simbolo == simbolo).first()


def get_moneda_list(db: Session) -> List[Moneda]:
    return db.query(Moneda).order_by(Moneda.nombre).all()
