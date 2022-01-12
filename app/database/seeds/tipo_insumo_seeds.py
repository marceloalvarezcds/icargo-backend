from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoInsumo


def tipo_insumo_seeds(db: Session):
    try:
        db.add(TipoInsumo(descripcion="COMBUSTIBLE"))
        db.add(TipoInsumo(descripcion="LUBRICANTES"))
        db.commit()
    except IntegrityError:
        db.rollback()
