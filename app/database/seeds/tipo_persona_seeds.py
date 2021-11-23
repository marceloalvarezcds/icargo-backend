from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoPersona


def tipo_persona_seeds(db: Session):
    try:
        db.add(TipoPersona(descripcion="Física"))
        db.add(TipoPersona(descripcion="Jurídica"))
        db.commit()
    except IntegrityError:
        db.rollback()
