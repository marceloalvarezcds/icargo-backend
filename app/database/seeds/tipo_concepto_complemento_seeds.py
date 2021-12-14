from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoConceptoComplemento


def tipo_concepto_complemento_seeds(db: Session):
    try:
        db.add(TipoConceptoComplemento(descripcion="Peaje"))
        db.add(TipoConceptoComplemento(descripcion="Expurgo"))
        db.commit()
    except IntegrityError:
        db.rollback()
