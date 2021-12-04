from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoCarga


def tipo_carga_seeds(db: Session):
    try:
        db.add(TipoCarga(descripcion="SECA"))
        db.add(TipoCarga(descripcion="LÍQUIDA"))
        db.commit()
    except IntegrityError:
        db.rollback()
