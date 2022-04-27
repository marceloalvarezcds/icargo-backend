from sqlalchemy.orm import Session  # type: ignore

from app.models import Moneda
from app.repositories import get_moneda_by_simbolo


def create_moneda(db: Session, nombre: str, simbolo: str):
    moneda = get_moneda_by_simbolo(db, simbolo)
    if moneda is None:
        moneda = Moneda(nombre=nombre, simbolo=simbolo)
        db.add(moneda)
        db.commit()


def moneda_seeds(db: Session):
    create_moneda(db, "Guaranies", "PYG")
    # create_moneda(db, "Dolares", "USD")
    # create_moneda(db, "Real", "BRL")
    # create_moneda(db, "Peso Argentino", "ARP")
    # create_moneda(db, "Peso Boliviano", "BOP")
