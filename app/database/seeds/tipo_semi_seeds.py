from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoSemi


def tipo_semi_seeds(db: Session):
    try:
        db.add(TipoSemi(descripcion="1D"))
        db.add(TipoSemi(descripcion="1D.1D"))
        db.add(TipoSemi(descripcion="1D.2D"))
        db.add(TipoSemi(descripcion="2D"))
        db.add(TipoSemi(descripcion="3D"))
        db.commit()
    except IntegrityError:
        db.rollback()
