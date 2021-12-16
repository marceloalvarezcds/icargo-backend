from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoAnticipo


def tipo_anticipo_seeds(db: Session):
    try:
        db.add(TipoAnticipo(descripcion="EFECTIVO"))
        db.add(TipoAnticipo(descripcion="COMBUSTIBLE"))
        db.add(TipoAnticipo(descripcion="LUBRICANTES"))
        db.add(TipoAnticipo(descripcion="OTROS"))
        db.commit()
    except IntegrityError:
        db.rollback()
