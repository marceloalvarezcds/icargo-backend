from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Moneda


def moneda_seeds(db: Session):
    try:
        db.add(Moneda(nombre="Guaranies", simbolo="PYG"))
        db.add(Moneda(nombre="Dolares", simbolo="USD"))
        db.add(Moneda(nombre="Real", simbolo="BRL"))
        db.add(Moneda(nombre="Peso Argentino", simbolo="ARP"))
        db.add(Moneda(nombre="Peso Boliviano", simbolo="BOP"))
        db.commit()
    except IntegrityError:
        db.rollback()
