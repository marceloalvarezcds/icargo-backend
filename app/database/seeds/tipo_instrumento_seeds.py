from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoInstrumento


def tipo_instrumento_seeds(db: Session):
    try:
        db.add(TipoInstrumento(descripcion="Cheque"))
        db.add(TipoInstrumento(descripcion="Transferencia"))
        db.commit()
    except IntegrityError:
        db.rollback()
