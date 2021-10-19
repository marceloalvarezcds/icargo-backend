from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Moneda


def moneda_seeds(db: Session):
    try:
        db.add(Moneda(nombre="Guaranies", simbolo="PYG"))
        db.add(Moneda(nombre="Dolares", simbolo="USD"))
        db.commit()
    except IntegrityError:
        db.rollback()
