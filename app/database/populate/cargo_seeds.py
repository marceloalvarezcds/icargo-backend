from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Cargo


def cargo_seeds(db: Session):
    try:
        db.add(Cargo(descripcion="Gerente"))
        db.add(Cargo(descripcion="Vendedor"))
        db.commit()
    except IntegrityError:
        db.rollback()
