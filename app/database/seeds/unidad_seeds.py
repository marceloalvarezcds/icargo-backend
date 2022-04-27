from decimal import Decimal

from sqlalchemy.orm import Session  # type: ignore

from app.models import Unidad
from app.repositories import get_unidad_by_descripcion


def create_unidad(db: Session, descripcion: str, abreviatura: str, conversion_kg):
    unidad = get_unidad_by_descripcion(db, descripcion)
    if unidad is None:
        unidad = Unidad(
            descripcion=descripcion,
            abreviatura=abreviatura,
            conversion_kg=conversion_kg,
        )
        db.add(unidad)
        db.commit()


def unidad_seeds(db: Session):
    create_unidad(db, "Kilogramos", "kg", Decimal(1))
    # create_unidad(db, "Toneladas", "Tm", Decimal(0.001))
    # create_unidad(db, "Litros", "lts", Decimal(1))
