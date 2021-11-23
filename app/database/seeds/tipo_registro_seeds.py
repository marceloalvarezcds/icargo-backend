from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoRegistro


def tipo_registro_seeds(db: Session):
    try:
        db.add(TipoRegistro(descripcion="Profesional A"))
        db.add(TipoRegistro(descripcion="Profesional B"))
        db.commit()
    except IntegrityError:
        db.rollback()
