from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoAnticipo


def tipo_anticipo_seeds(db: Session):
    try:
        db.add(TipoAnticipo(descripcion="EFECTIVO"))
        db.add(TipoAnticipo(descripcion="INSUMOS"))
        db.commit()
    except IntegrityError:
        db.rollback()
