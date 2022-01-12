from decimal import Decimal

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Unidad


def unidad_seeds(db: Session):
    try:
        db.add(
            Unidad(
                descripcion="Toneladas", abreviatura="Tm", conversion_kg=Decimal(0.001)
            )
        )
        db.add(
            Unidad(descripcion="Kilogramos", abreviatura="kg", conversion_kg=Decimal(1))
        )
        db.add(
            Unidad(descripcion="Litros", abreviatura="lts", conversion_kg=Decimal(1))
        )
        db.commit()
    except IntegrityError:
        db.rollback()
