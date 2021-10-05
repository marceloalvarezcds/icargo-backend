from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Pais

from .localidad_seeds import (
    localidad_argentina_seeds,
    localidad_brasil_seeds,
    localidad_paraguay_seeds,
)


def pais_seeds(db: Session):
    try:
        paraguay = Pais(nombre="Paraguay", nombre_corto="PY")
        argentina = Pais(nombre="Argentina", nombre_corto="AR")
        brasil = Pais(nombre="Brasil", nombre_corto="BR")
        db.add(paraguay)
        db.add(argentina)
        db.add(brasil)
        db.commit()
        localidad_paraguay_seeds(db, paraguay)
        localidad_argentina_seeds(db, argentina)
        localidad_brasil_seeds(db, brasil)
    except IntegrityError:
        db.rollback()
