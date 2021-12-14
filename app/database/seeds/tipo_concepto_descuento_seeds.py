from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoConceptoDescuento


def tipo_concepto_descuento_seeds(db: Session):
    try:
        db.add(TipoConceptoDescuento(descripcion="Sistema"))
        db.add(TipoConceptoDescuento(descripcion="Seguro"))
        db.commit()
    except IntegrityError:
        db.rollback()
